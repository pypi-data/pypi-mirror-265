use pyo3::prelude::*;
use raftify::ClusterJoinTicket;
use std::collections::HashMap;

use super::peers::PyPeers;

#[derive(Clone)]
#[pyclass(name = "ClusterJoinTicket")]
pub struct PyClusterJoinTicket {
    pub inner: ClusterJoinTicket,
}

#[pymethods]
impl PyClusterJoinTicket {
    #[new]
    pub fn new(reserved_id: u64, raft_addr: String, leader_addr: String, peers: PyPeers) -> Self {
        let peers = peers
            .inner
            .inner
            .iter()
            .map(|(id, peer)| (*id, peer.addr))
            .collect::<HashMap<_, _>>();

        PyClusterJoinTicket {
            inner: ClusterJoinTicket {
                reserved_id,
                raft_addr,
                leader_addr,
                peers,
            },
        }
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self.inner)
    }

    pub fn get_reserved_id(&self) -> u64 {
        self.inner.reserved_id
    }
}
