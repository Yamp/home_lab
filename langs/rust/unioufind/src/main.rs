extern crate disjoint_sets;

use disjoint_sets::UnionFind;

struct UFForPython {
    data: UnionFind
}

impl UFForPython {
    fn new(len: usize) -> UFForPython {
        UFForPython {
            data: disjoint_sets::UnionFind::new(len)
        }
    }

    fn connected(&self, i: usize, j: usize) -> bool { self.data.equiv(i, j) }

    fn union(&mut self, i: usize, j: usize) { self.data.union(i, j); }

    fn find(&self, i: usize) -> usize { self.data.find(i) }
}

fn main() {
    let mut set = UFForPython::new(10);
    println!("finding {} {}", set.find(1), set.find(2));
    set.union(1, 2);
    set.union(3, 4);
    set.union(1, 4);
    assert!(set.connected(1, 2));
    assert!(set.connected(3, 4));
    assert!(set.connected(2, 3));

    assert!(!set.connected(1, 5));
    assert!(!set.connected(5, 6));
    println!("Good!");
}
