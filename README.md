# Raft
***
In my attempt to understand the Raft algorithm, I am planning 
to write it's implementation in Python. 

> Consensus algorith allows collection of Machines [ Cluster ] to work
> as a coherent group that can survive failure of some of it's members

A node can be in a one of the three states 
- Candidate 
- Leader 
- Follower 

# Process
- All nodes start in follower state.
- If the followers don't hear from the leader, they become candidate
- candidate request votes from the other nodes.
- Nodes will reply with the votes 
- Candidate becomes leader if it receive votes from majority of the nodes. 
- This is what it called as leader election.
- Once the leader is elected, all changes to the system will go through leader
- Each change is added as an entry in the Node's logs 
- The log entry is uncommitted, so it won't update the node's value 
- To commit entry, the leader first replicates entry to followe nodes. 
- Leader waits till majority of the nodes have written the entry 
- Entry is now committed to the leader node
- Leader then notifies followers that Entry is committed
- The cluster now has come to consensus about the system state
- This process is called as Log replication

***
# Leader Election
- In Raft there are two timeouts settings which control elections 
- The first is election timeout, is the amount of time follower waits before 
  becoming the candidate 
- The election timeout is randomized between 150ms to 300ms 
- After this timeout, follower becomes a candidate and starts a new election term
- Votes for itself 
- And then sends out request vote messages to other nodes 
- If the receiving node hasn't voted for this term, then it votes for the candidate
- And then it resets its election timeout 
- Once the candidate has majority of the votes, it becomes leader. 
- The leader starts sending out append entries to followers 
- These messages are sent in the intervals specified by Hearbeat timeout
- Followers respond to each AppendEntry message 
- The election term will continue untill follower stops receiving hearbeats and 
  becomes candidate
- Requiring majority of votes garuntees that only one leader can be elected per term
- If two nodes become, candidate at the same time, a split vote can happen
- In that case finally election timeout will happen and then election will restart

***
# Log Replication
- Once we have the leader, it needs to replicate all changes to our system to all 
  the nodes 
- This is done by using the same AppendEntry message that was used for HeartBeats
- First client sends a change to the leader
- The change is appended to leader's log 
- Then the change is sent to followers on the next heartbeat 
- An Entry is committed once the majority of the followers ack it. 
- And a response is then sent to client 
- 

> Basically there is concept of election where you declare your candidature 
> Post the election, **Node** is either a Leader or a Follower until further notice 
> Where something happens with the current leader / there is re-election

## Candidate
***


## Leader 
***


## Follower 
*** 


## Replicated Log 
***

## Client interaction
[Source](https://eli.thegreenplace.net/2020/implementing-raft-part-0-introduction/)

Earlier, I said "Instead of contacting a single server to perform a service, clients will contact the whole cluster"; but what does this mean? A cluster is just a group of servers connected over the network, so how do you contact "the whole cluster"?

The answer is simple:

- When working with a Raft cluster, a client knows the network addresses of the cluster's replicas. How it knows this (e.g. by using some sort of service discovery mechanism) it out of scope for this post.
- A client initially sends a request to an arbitrary replica. If this replica is the leader, it acknowledges the request immediately and the client will wait for a full response. After that, the client remembers that this replica is the leader and won't have to search for it again (until some failure, like leader crash).
- If the replica says it's not the leader, the client will try another replica. A possible optimization here is that a follower replica can tell the client which other replica is the leader. Since replicas communicate continuously among themselves, typically it knows the right answer. This can save the client a couple of guesses.
- Another case in which the client may realize the replica it contacted is not the leader is if it's request is not committed within some timeout. This may mean the replica it contacted is not actually the leader (even if it still thinks it is) - it may have been partitioned from the other Raft servers. When the timeout elapses, the client will go on searching for a different leader again.

The optimization mentioned in the third bullet point is not necessary in most cases.
In general, it's useful to distinguish between "normal operation" and "fault scenario"
in Raft. A typical service will spend over 99.9% of its time in "normal operation",
where clients know who the leader is because they have this information cached from
back when they first contacted the service. Fault scenarios - which we'll discuss in
more detail in the next section - definitely muddle the waters, but only for a short
while. As we'll learn in detail in the next posts, a Raft cluster will recover from
a temporary server failure or network partition very quickly - in well under a second
in most scenarios. There will be a short blip of unavailability while the new leader
asserts its leadership and clients find which server it is, but afterwards it will go
back to the "normal operation mode"


## Resources 
***
- https://raft.github.io/raft.pdf
- https://eli.thegreenplace.net/2020/implementing-raft-part-0-introduction/
- https://raft.github.io/
- 