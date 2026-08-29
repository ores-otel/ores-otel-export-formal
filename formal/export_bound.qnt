module export_bound {
  type ExportPhase = Accepting | Draining | Stopped

  var queued: int
  var export_phase: ExportPhase

  val capacity = 8

  action init = all {
    queued' = 0,
    export_phase' = Accepting,
  }

  action step = {
    any {
      all {
        export_phase == Accepting,
        queued < capacity,
        queued' = queued + 1,
        export_phase' = export_phase,
      },
      all {
        export_phase == Accepting,
        queued' = queued,
        export_phase' = Draining,
      },
      all {
        or {
          export_phase == Accepting,
          export_phase == Draining,
        },
        queued > 0,
        queued' = queued - 1,
        export_phase' = export_phase,
      },
      all {
        export_phase == Draining,
        queued == 0,
        queued' = queued,
        export_phase' = Stopped,
      },
      all {
        queued' = queued,
        export_phase' = export_phase,
      },
    }
  }

  val queue_within_capacity = queued >= 0 and queued <= capacity

  val stopped_is_empty = or {
    export_phase != Stopped,
    queued == 0,
  }
}
