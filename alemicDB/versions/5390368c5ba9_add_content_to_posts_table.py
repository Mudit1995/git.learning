"""add content to posts table 

Revision ID: 5390368c5ba9
Revises: 9b64fa81a3a4
Create Date: 2023-09-29 17:44:31.637755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5390368c5ba9'
down_revision: Union[str, None] = '9b64fa81a3a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_columnn('posts','content')
    pass
