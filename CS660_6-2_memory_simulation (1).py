"""CS 660 Module 6-2: Concurrent memory allocation and mark-and-sweep simulation.

This is a *simulation* of a small shared heap. Python still manages the real
memory used by this script. Simulated roots and object IDs, not Python's GC,
control which simulated objects are retained or reclaimed.
"""

from dataclasses import dataclass, field
from threading import Barrier, BrokenBarrierError, Lock, Thread, current_thread


@dataclass
class MemoryObject:
    """A simulated heap record, reachable through object IDs."""

    object_id: int
    description: str
    references: set[int] = field(default_factory=set)
    marked: bool = False


class SharedMemoryPool:
    """Track simulated allocations, roots, and synchronized collections."""

    def __init__(self) -> None:
        self.objects: dict[int, MemoryObject] = {}
        self.roots: dict[str, set[int]] = {}
        self.lock = Lock()
        self.next_id = 1
        self.allocation_count = 0
        self.reclaimed_count = 0

    def allocate(self, description: str, rooted: bool = True) -> int:
        """Allocate a record, optionally registering a thread-owned root."""
        owner = current_thread().name
        with self.lock:
            object_id = self.next_id
            self.next_id += 1
            self.objects[object_id] = MemoryObject(object_id, description)
            self.allocation_count += 1
            if rooted:
                self.roots.setdefault(owner, set()).add(object_id)
            print(f"[{owner}] ALLOCATE  id={object_id:02d}  "
                  f"{description}  rooted={rooted}")
            return object_id

    def link(self, source_id: int, target_id: int) -> None:
        """Make one simulated object refer to another."""
        owner = current_thread().name
        with self.lock:
            if source_id not in self.objects or target_id not in self.objects:
                raise KeyError("Both simulated objects must exist to create a link")
            self.objects[source_id].references.add(target_id)
            print(f"[{owner}] LINK      id={source_id:02d} -> id={target_id:02d}")

    def release_root(self, object_id: int) -> None:
        """Release a simulated thread root without immediately deleting it."""
        owner = current_thread().name
        with self.lock:
            if object_id not in self.roots.get(owner, set()):
                raise ValueError(f"Object {object_id} is not a root for {owner}")
            self.roots[owner].remove(object_id)
            print(f"[{owner}] RELEASE   root id={object_id:02d}")

    def mark_and_sweep(self, cycle: int) -> tuple[int, int]:
        """Mark objects reachable from all roots, then sweep unmarked ones.

        Locking the full cycle models a stop-the-world collector: mutator
        threads cannot change the simulated heap during tracing or sweeping.
        """
        with self.lock:
            print(f"\n[Collector] ===== COLLECTION CYCLE {cycle} =====")
            for obj in self.objects.values():
                obj.marked = False

            pending = [obj_id for thread_roots in self.roots.values()
                       for obj_id in thread_roots]
            while pending:
                obj_id = pending.pop()
                obj = self.objects.get(obj_id)
                if obj is None or obj.marked:
                    continue
                obj.marked = True
                pending.extend(obj.references)
                print(f"[Collector] MARK      reachable id={obj_id:02d}")

            garbage_ids = sorted(obj_id for obj_id, obj in self.objects.items()
                                 if not obj.marked)
            for obj_id in garbage_ids:
                del self.objects[obj_id]
                self.reclaimed_count += 1
                print(f"[Collector] SWEEP     reclaimed id={obj_id:02d}")

            survivors = len(self.objects)
            print(f"[Collector] RESULT    reclaimed={len(garbage_ids)} "
                  f"survivors={survivors}\n")
            return len(garbage_ids), survivors


def worker(pool: SharedMemoryPool, ready: Barrier, resume: Barrier,
           final_ready: Barrier) -> None:
    """Allocate a rooted parent, its child, and an abandoned temporary."""
    owner = current_thread().name
    anchor = pool.allocate(f"{owner} parent", rooted=True)
    child = pool.allocate(f"{owner} child", rooted=False)
    pool.link(anchor, child)  # Child remains live through the rooted parent.
    temporary = pool.allocate(f"{owner} temporary", rooted=True)
    pool.release_root(temporary)  # Unreachable at the first collection.
    ready.wait(timeout=15)
    resume.wait(timeout=15)  # Collector finished preserving parent + child.
    pool.release_root(anchor)  # Parent and child are now unreachable.
    final_ready.wait(timeout=15)


def collector(pool: SharedMemoryPool, ready: Barrier,
              resume: Barrier, final_ready: Barrier) -> None:
    """Run one collection with roots, then another after roots are dropped."""
    ready.wait(timeout=15)
    first_freed, first_remaining = pool.mark_and_sweep(cycle=1)
    assert (first_freed, first_remaining) == (3, 6)
    resume.wait(timeout=15)
    final_ready.wait(timeout=15)
    second_freed, second_remaining = pool.mark_and_sweep(cycle=2)
    assert (second_freed, second_remaining) == (6, 0)


def main() -> None:
    pool = SharedMemoryPool()
    ready, resume, final_ready = Barrier(4), Barrier(4), Barrier(4)
    workers = [Thread(target=worker, name=f"Worker-{number}",
                      args=(pool, ready, resume, final_ready))
               for number in range(1, 4)]
    gc_thread = Thread(target=collector, name="Collector",
                       args=(pool, ready, resume, final_ready))

    print("CS 660 | Shared-memory simulation with 3 workers and 1 collector")
    for thread in workers + [gc_thread]:
        thread.start()
    for thread in workers + [gc_thread]:
        thread.join()

    with pool.lock:
        print("=== FINAL SUMMARY ===")
        print(f"Total allocations: {pool.allocation_count}")
        print(f"Total reclaimed:   {pool.reclaimed_count}")
        print(f"Objects remaining: {len(pool.objects)}")
        assert pool.allocation_count == 9
        assert pool.reclaimed_count == 9
        assert len(pool.objects) == 0
        print("PASS: all reachable objects survived cycle 1; "
              "all abandoned objects were reclaimed by cycle 2.")


if __name__ == "__main__":
    main()
