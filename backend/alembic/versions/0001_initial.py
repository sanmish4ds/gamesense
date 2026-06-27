"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-27
"""

from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "teams",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("short_name", sa.String(10)),
        sa.Column("country", sa.String(50)),
        sa.Column("logo_url", sa.String(500)),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "players",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("full_name", sa.String(200)),
        sa.Column("country", sa.String(50)),
        sa.Column("role", sa.String(50)),
        sa.Column("batting_style", sa.String(50)),
        sa.Column("bowling_style", sa.String(50)),
        sa.Column("team_id", sa.String(), sa.ForeignKey("teams.id")),
        sa.Column("date_of_birth", sa.String(20)),
        sa.Column("image_url", sa.String(500)),
        sa.Column("batting_avg", sa.Float()),
        sa.Column("bowling_avg", sa.Float()),
        sa.Column("batting_sr", sa.Float()),
        sa.Column("economy", sa.Float()),
        sa.Column("matches", sa.Integer(), default=0),
        sa.Column("runs", sa.Integer(), default=0),
        sa.Column("wickets", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "matches",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("match_type", sa.String(20)),
        sa.Column("status", sa.String(50)),
        sa.Column("venue", sa.String(200)),
        sa.Column("date", sa.String(30)),
        sa.Column("date_time_gmt", sa.String(50)),
        sa.Column("team1_id", sa.String()),
        sa.Column("team1_name", sa.String(100)),
        sa.Column("team2_id", sa.String()),
        sa.Column("team2_name", sa.String(100)),
        sa.Column("is_live", sa.Boolean(), default=False),
        sa.Column("score", sa.JSON()),
        sa.Column("toss", sa.JSON()),
        sa.Column("current_over", sa.Float()),
        sa.Column("batting_team", sa.String(100)),
        sa.Column("bowling_team", sa.String(100)),
        sa.Column("match_winner", sa.String(200)),
        sa.Column("scorecard", sa.JSON()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "ball_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("match_id", sa.String(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("over", sa.Integer(), nullable=False),
        sa.Column("ball", sa.Integer(), nullable=False),
        sa.Column("innings", sa.Integer(), nullable=False, default=1),
        sa.Column("batsman", sa.String(100)),
        sa.Column("bowler", sa.String(100)),
        sa.Column("runs", sa.Integer(), default=0),
        sa.Column("extras", sa.Integer(), default=0),
        sa.Column("extra_type", sa.String(20)),
        sa.Column("is_wicket", sa.Boolean(), default=False),
        sa.Column("wicket_type", sa.String(50)),
        sa.Column("wicket_player", sa.String(100)),
        sa.Column("is_boundary", sa.Boolean(), default=False),
        sa.Column("is_six", sa.Boolean(), default=False),
        sa.Column("total_runs", sa.Integer(), default=0),
        sa.Column("total_wickets", sa.Integer(), default=0),
        sa.Column("run_rate", sa.Float()),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_ball_events_match_innings", "ball_events", ["match_id", "innings", "over", "ball"])


def downgrade():
    op.drop_index("ix_ball_events_match_innings", "ball_events")
    op.drop_table("ball_events")
    op.drop_table("matches")
    op.drop_table("players")
    op.drop_table("teams")
