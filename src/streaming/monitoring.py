"""lecture 20: Consumer Lag Monitoring — testable ფორმატირება, AdminClient-ისგან დამოუკიდებელი."""
from dataclasses import dataclass

@dataclass
class PartitionLag:
    partition: int
    end_offset: int
    committed_offset: int

    @property
    def lag(self) -> int:
        return self.end_offset - self.committed_offset

def format_lag_report(group_id: str, topic: str, partitions: list[PartitionLag]) -> str:
    """
    partitions: PartitionLag-ების სია (AdminClient-იდან რეალურად წამოსული რიცხვები,
    ან ტესტში — ხელით აწყობილი). აბრუნებს ადამიანისთვის წაკითხვად რეპორტს.
    """
    lines = [f"Consumer Lag Report — group='{group_id}', topic='{topic}'"]
    total_lag = 0
    for p in sorted(partitions, key=lambda x: x.partition):
        status = "⚠ ჩამორჩენილია" if p.lag > 0 else "✓ განახლებულია"
        lines.append(f"  partition {p.partition}: end={p.end_offset}, committed={p.committed_offset}, lag={p.lag} {status}")
        total_lag += p.lag
    lines.append(f"სულ lag: {total_lag}")
    return "\n".join(lines)
