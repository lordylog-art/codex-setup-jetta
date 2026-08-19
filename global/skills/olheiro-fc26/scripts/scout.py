#!/usr/bin/env python3
"""Filtra e ranqueia jogadores do relatório mundial FC26 sem inventar dados."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def latest_report() -> Path:
    profile = Path(os.environ.get("USERPROFILE", Path.home()))
    roots = [
        Path(os.environ.get(name, "")) / "Desktop"
        for name in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial")
        if os.environ.get(name)
    ]
    roots += [profile / "OneDrive" / "Desktop", profile / "Desktop"]
    files: list[Path] = []
    for root in roots:
        folder = root / "FC26_OLHEIRO"
        if folder.is_dir():
            files.extend(folder.glob("MUNDO_FC26_*.json"))
    if not files:
        raise FileNotFoundError("Nenhum MUNDO_FC26_*.json encontrado em Desktop\\FC26_OLHEIRO")
    return max(files, key=lambda item: item.stat().st_mtime)


def csv_set(value: str | None) -> set[str]:
    return {item.strip().casefold() for item in (value or "").split(",") if item.strip()}


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def parse_attributes(items: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    for item in items:
        if ":" not in item:
            raise ValueError(f"Atributo inválido: {item}; use campo:mínimo")
        field, minimum = item.split(":", 1)
        result[field.strip().casefold()] = float(minimum)
    return result


def player_positions(player: dict) -> set[str]:
    positions = player.get("positions") or {}
    values = []
    if positions.get("primary"):
        values.append(positions["primary"])
    values.extend(positions.get("alternatives") or [])
    return {str(item.get("name", "")).casefold() for item in values if isinstance(item, dict)}


def matches_range(value, minimum, maximum) -> bool:
    if value is None:
        return minimum is None and maximum is None
    return (minimum is None or value >= minimum) and (maximum is None or value <= maximum)


def candidate(player: dict, args, required_attributes: dict[str, float], user_team_id):
    ratings = player.get("ratings") or {}
    attributes = {str(k).casefold(): v for k, v in (player.get("attributes") or {}).items()}
    playstyles = player.get("playstyles") or {}
    regular = {str(item).casefold() for item in playstyles.get("regular") or []}
    plus = {str(item).casefold() for item in playstyles.get("plus") or []}
    positions = player_positions(player)
    club = player.get("club") or {}
    financials = player.get("financials") or {}
    overall, potential, age = number(ratings.get("overall")), number(ratings.get("potential")), number(player.get("age"))

    if args.exclude_user_team and user_team_id is not None and club.get("teamid") == user_team_id:
        return None
    if args.positions and not (positions & args.positions):
        return None
    if not matches_range(age, args.min_age, args.max_age):
        return None
    if not matches_range(overall, args.min_overall, args.max_overall):
        return None
    if not matches_range(potential, args.min_potential, args.max_potential):
        return None
    if not args.playstyles.issubset(regular | plus):
        return None
    if not args.plus.issubset(plus):
        return None
    stars = player.get("stars") or {}
    if args.min_skill_moves is not None and (number(stars.get("skill_moves")) or -1) < args.min_skill_moves:
        return None
    if args.min_weak_foot is not None and (number(stars.get("weak_foot")) or -1) < args.min_weak_foot:
        return None
    physical = player.get("physical") or {}
    if args.preferred_foot is not None and physical.get("preferred_foot_code") != args.preferred_foot:
        return None
    for field, minimum in required_attributes.items():
        if number(attributes.get(field)) is None or attributes[field] < minimum:
            return None

    market_value = number(financials.get("market_value"))
    release_clause = number(financials.get("release_clause"))
    comparable_value = market_value if market_value is not None else release_clause
    if args.budget is not None and comparable_value is not None and comparable_value > args.budget:
        return None

    score = (overall or 0) * 1.2 + (potential or overall or 0) * 0.8
    if overall is not None and potential is not None:
        score += max(0, potential - overall) * 1.5
    score += len(args.playstyles & (regular | plus)) * 4
    score += len(args.plus & plus) * 9
    score += sum(max(0, attributes[field] - minimum) * 0.08 for field, minimum in required_attributes.items())
    if age is not None and age <= 21:
        score += 4
    if args.budget is not None and comparable_value is None:
        score -= 3

    return {
        "playerid": player.get("playerid"),
        "name": player.get("name"),
        "club": club or None,
        "age": age,
        "overall": overall,
        "potential": potential,
        "positions": sorted(positions),
        "playstyles": playstyles.get("regular") or [],
        "playstyles_plus": playstyles.get("plus") or [],
        "market_value": market_value,
        "release_clause": release_clause,
        "wage": number(financials.get("wage")),
        "budget_status": "unknown" if comparable_value is None else "within_budget",
        "matched_attributes": {field: attributes[field] for field in required_attributes},
        "fit_score": round(score, 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Olheiro determinístico para relatório mundial do FC 26")
    parser.add_argument("--json", type=Path, help="Relatório; omita para usar o mais recente")
    parser.add_argument("--positions", help="Posições separadas por vírgula, ex.: ST,CF")
    parser.add_argument("--min-age", type=int)
    parser.add_argument("--max-age", type=int)
    parser.add_argument("--min-overall", type=int)
    parser.add_argument("--max-overall", type=int)
    parser.add_argument("--min-potential", type=int)
    parser.add_argument("--max-potential", type=int)
    parser.add_argument("--budget", type=float, help="Orçamento máximo na unidade monetária do save")
    parser.add_argument("--playstyles", help="PlayStyles aceitos regular ou Plus")
    parser.add_argument("--plus", help="PlayStyles obrigatoriamente Plus")
    parser.add_argument("--attribute", action="append", default=[], help="campo:mínimo; pode repetir")
    parser.add_argument("--min-skill-moves", type=int)
    parser.add_argument("--min-weak-foot", type=int)
    parser.add_argument("--preferred-foot", type=int, choices=(1, 2), help="Código bruto do pé preferido")
    parser.add_argument("--exclude-user-team", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    args.positions = csv_set(args.positions)
    args.playstyles = csv_set(args.playstyles)
    args.plus = csv_set(args.plus)
    required_attributes = parse_attributes(args.attribute)

    path = args.json or latest_report()
    with path.open("r", encoding="utf-8-sig") as handle:
        report = json.load(handle)
    if report.get("scope") != "all_world_players_in_loaded_save" or not isinstance(report.get("players"), list):
        raise ValueError("JSON não é um relatório mundial compatível")
    user_team_id = (report.get("user_team") or {}).get("teamid")
    candidates = [
        item for player in report["players"]
        if (item := candidate(player, args, required_attributes, user_team_id)) is not None
    ]
    candidates.sort(key=lambda item: (-item["fit_score"], -(item["potential"] or -1), -(item["overall"] or -1), item["playerid"] or 0))
    output = {
        "report_path": str(path.resolve()),
        "generated_at": report.get("generated_at"),
        "world_player_count": report.get("player_count"),
        "match_count": len(candidates),
        "returned_count": min(len(candidates), max(0, args.limit)),
        "financial_warning": "unknown significa que o save não forneceu valor comparável; não é estimativa",
        "candidates": candidates[: max(0, args.limit)],
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
