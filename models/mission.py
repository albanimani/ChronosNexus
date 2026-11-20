
class Mission:
    def __init__(
        self,
        name,
        origin,
        destination,
        cargo_type,
        cargo_amount,
        deadline,
        priority,
        importance,
        required_capabilities
    ):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cargo_type = cargo_type
        self.cargo_amount = cargo_amount
        self.deadline = deadline
        self.priority = priority
        self.importance = importance
        self.required_capabilities = required_capabilities
        self.status = "pending"
        self.assigned_spacecraft = None
        self.departure_time = None

    def assign_spacecraft(self, spacecraft, departure_time):
        self.assigned_spacecraft = spacecraft
        self.departure_time = departure_time
        self.status = "assigned"

    def complete_mission(self):
        self.status = "completed"

    def is_overdue(self, current_time):
        return current_time > self.deadline and self.status != "completed"
