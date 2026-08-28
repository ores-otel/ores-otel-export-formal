module export_bound {
  var queued: int
  val capacity = 8

  action init = {
    queued' = 0
  }

  action step = {
    any {
      queued < capacity and queued' = queued + 1,
      queued > 0 and queued' = queued - 1,
      queued' = queued,
    }
  }

  val queue_within_capacity = queued >= 0 and queued <= capacity
}
