"""empty message

Revision ID: 5a178ef4e19c
Revises: 4458f5a0d799
Create Date: 2018-07-14 10:00:13.331264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a178ef4e19c'
down_revision = '4458f5a0d799'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ihome_area',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ihome_facility',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('css', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ihome_house',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=512), nullable=True),
    sa.Column('room_count', sa.Integer(), nullable=True),
    sa.Column('acreage', sa.Integer(), nullable=True),
    sa.Column('unit', sa.String(length=32), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=True),
    sa.Column('beds', sa.String(length=64), nullable=True),
    sa.Column('deposit', sa.Integer(), nullable=True),
    sa.Column('min_days', sa.Integer(), nullable=True),
    sa.Column('max_days', sa.Integer(), nullable=True),
    sa.Column('order_count', sa.Integer(), nullable=True),
    sa.Column('index_image_url', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['ihome_area.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ihome_house_facility',
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('facility_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['facility_id'], ['ihome_facility.id'], ),
    sa.ForeignKeyConstraint(['house_id'], ['ihome_house.id'], ),
    sa.PrimaryKeyConstraint('house_id', 'facility_id')
    )
    op.create_table('ihome_house_image',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['ihome_house.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ihome_order',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('begin_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('days', sa.Integer(), nullable=False),
    sa.Column('house_price', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('待接单', '待支付', '已支付', '待评价', '已完成', '已取消', '已拒单'), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['house_id'], ['ihome_house.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ihome_order_status'), 'ihome_order', ['status'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ihome_order_status'), table_name='ihome_order')
    op.drop_table('ihome_order')
    op.drop_table('ihome_house_image')
    op.drop_table('ihome_house_facility')
    op.drop_table('ihome_house')
    op.drop_table('ihome_facility')
    op.drop_table('ihome_area')
    # ### end Alembic commands ###