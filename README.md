# hungarian-room-drafting

This project uses the [Hungarian Algorithm](https://en.wikipedia.org/wiki/Hungarian_algorithm) to assign people to rooms based on their ranked preferences and budget constraints. It computes all possible optimal assignments that minimize the total "unhappiness" (sum of rankings), taking budgets into account.

---

## 📥 Input Format

The input is a CSV file exported from a Google Form. Each row represents one person's rankings and budget:

| Timestamp | Name | [B Small] | [B Medium] | [B Large] | [1st Small] | [1st Large] | [2nd Large] | [2nd Small 1] | [2nd Small 2] | [Master] | Budget |
|-----------|------|-----------|------------|-----------|--------------|--------------|---------------|----------------|----------------|----------|--------|
| 2025-05-12 10:00:00 | Alice | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | $1,500 |

- Each `[Room Name]` column is a ranking (1 = most preferred)
- The **Budget** is a string like `$1,500`, `1500`, or `No limit`

Rooms that exceed someone's budget are excluded from their assignment options.

---

## 🛠 How to Run

```bash
python assign_housing.py
