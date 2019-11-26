extern crate disjoint_sets;

use disjoint_sets::UnionFind;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;


#[pyclass(module="union_find_py")]
struct UFForPython {
    data: UnionFind
}

#[pymethods]
impl UFForPython {
    #[new]
    fn new(obj: &PyRawObject, len: usize) {
        obj.init({
            UFForPython {
                data: disjoint_sets::UnionFind::new(len)
            }
        });
    }

    fn connected(&self, i: usize, j: usize) -> PyResult<bool> {
        let res = self.data.equiv(i, j);
        Ok(res)
    }

    fn union(&mut self, i: usize, j: usize) -> PyResult<()> {
        self.data.union(i, j);
        Ok(())
    }

    fn find(&self, i: usize) -> PyResult<usize> {
        let res = self.data.find(i);
        Ok(res)
    }
}

/// This module is a python module implemented in Rust.
#[pymodule]
fn union_find_py(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<UFForPython>()?;

    Ok(())
}
