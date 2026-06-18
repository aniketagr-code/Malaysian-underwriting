import aiosqlite
import json

import os

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "underwriting_audit.db")

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                scorecard_version TEXT,
                request_payload TEXT,
                decision TEXT,
                composite_score INTEGER,
                reinsurance_referral BOOLEAN,
                audit_waterfall TEXT,
                total_payable REAL
            )
        ''')
        await db.commit()

async def log_quote(req_data: dict, result: dict):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''
            INSERT INTO audit_logs (scorecard_version, request_payload, decision, composite_score, reinsurance_referral, audit_waterfall, total_payable)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.get("scorecard_version"),
            json.dumps(req_data),
            result.get("decision"),
            result.get("composite_score"),
            result.get("reinsurance_referral"),
            json.dumps(result.get("premium_breakdown", {})) if "premium_breakdown" in result else None,
            result.get("premium_breakdown", {}).get("total_payable") if "premium_breakdown" in result else None
        ))
        await db.commit()
