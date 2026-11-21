class DynamicEvent:
    def __init__(
        self,
        name,
        event_type,
        affected_location,
        description,
        impact,
        start_time,
        duration
    ):
        self.name = name
        self.event_type = event_type
        self.affected_location = affected_location
        self.description = description
        self.impact = impact
        self.start_time = start_time
        self.duration = duration
        self.status = "pending"

    def activate_event(self):
        self.status = "active"

    def complete_event(self):
        self.status = "completed"

    def is_active(self, current_time):
        return (
            self.status == "active"
            and self.start_time <= current_time
            and current_time <= self.start_time + self.duration
        )