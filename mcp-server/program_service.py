from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from threading import Lock


class ProgramStatus(str, Enum):
    ACTIVE = "active"
    ACTIVATED = "activated"
    EXPIRED = "expired"
    INVALID = "invalid"


@dataclass
class Program:
    program_id: str
    description: str
    expires_at: datetime
    status: ProgramStatus = ProgramStatus.ACTIVE
    activated_at: datetime | None = None
    activated_by: str | None = None


@dataclass
class ActivationResult:
    success: bool
    program_id: str
    message: str
    status: ProgramStatus
    benefit: str | None = None
    description: str | None = None
    activated_at: str | None = None

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "program_id": self.program_id,
            "message": self.message,
            "status": self.status.value,
            "benefit": self.benefit,
            "description": self.description,
            "activated_at": self.activated_at,
        }


class ProgramStore:
    """In-memory program store for demo and local development."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._programs: dict[str, Program] = {}
        self._seed_demo_programs()

    def _seed_demo_programs(self) -> None:
        now = datetime.now(timezone.utc)
        demo_programs = [
            Program(
                program_id="COKE-SUMMER-2026",
                description="Summer Refresh Program",
                expires_at=datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
            ),
            Program(
                program_id="COKE-WELCOME-PROGRAM",
                description="Welcome Program for new customers",
                expires_at=datetime(2026, 9, 30, 23, 59, 59, tzinfo=timezone.utc),
            ),
            Program(
                program_id="COKE-LEGACY-2025",
                description="Legacy Rewards Program",
                expires_at=datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
            ),
        ]
        for program in demo_programs:
            if program.expires_at < now:
                program.status = ProgramStatus.EXPIRED
            self._programs[program.program_id.upper()] = program

    def activate(self, program_id: str, user_id: str = "end-user") -> ActivationResult:
        normalized_id = program_id.strip().upper()
        if not normalized_id:
            return ActivationResult(
                success=False,
                program_id=program_id,
                message="Program ID is required.",
                status=ProgramStatus.INVALID,
            )

        with self._lock:
            program = self._programs.get(normalized_id)
            print(f"Attempting to activate program '{program}' for user '{user_id}'")
            if program is None:
                return ActivationResult(
                    success=False,
                    program_id=normalized_id,
                    message=f"Program '{normalized_id}' was not found.",
                    status=ProgramStatus.INVALID,
                )

            now = datetime.now(timezone.utc)
            if program.expires_at < now and program.status != ProgramStatus.ACTIVATED:
                program.status = ProgramStatus.EXPIRED
                return ActivationResult(
                    success=False,
                    program_id=normalized_id,
                    message=f"Program '{normalized_id}' has expired.",
                    status=ProgramStatus.EXPIRED,
                    description=program.description
                )

            if program.status == ProgramStatus.ACTIVATED:
                print(f"Program '{normalized_id}' was already activated.")
                activated_at = program.activated_at.isoformat() if program.activated_at else None
                return ActivationResult(
                    success=False,
                    program_id=normalized_id,
                    message=f"Program '{normalized_id}' was already activated.",
                    status=ProgramStatus.ACTIVATED,
                    description=program.description,
                    activated_at=activated_at,
                )

            program.status = ProgramStatus.ACTIVATED
            program.activated_at = now
            program.activated_by = user_id

            return ActivationResult(
                success=True,
                program_id=normalized_id,
                message=f"Program '{normalized_id}' activated successfully.",
                status=ProgramStatus.ACTIVATED,
                description=program.description,
                activated_at=now.isoformat(),
            )


program_store = ProgramStore()
