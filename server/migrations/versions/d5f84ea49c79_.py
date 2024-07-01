"""reinitialize db

Revision ID: d5f84ea49c79
Revises: 
Create Date: 2024-07-01 15:06:54.576715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f84ea49c79'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feed',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=128), nullable=False),
                    sa.Column('url', sa.String(length=512), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('url')
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=254), nullable=False),
                    sa.Column('username', sa.String(
                        length=64), nullable=False),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )
    op.create_table('article',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=128), nullable=False),
                    sa.Column('author', sa.String(length=128), nullable=False),
                    sa.Column('pub_date', sa.DateTime(), nullable=False),
                    sa.Column('url', sa.String(length=512), nullable=False),
                    sa.Column('feed_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('url')
                    )
    op.create_table('user_feed',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('feed_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_feed')
    op.drop_table('article')
    op.drop_table('user')
    op.drop_table('feed')
    # ### end Alembic commands ###
