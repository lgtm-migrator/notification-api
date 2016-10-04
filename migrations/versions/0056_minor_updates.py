"""empty message

Revision ID: 0056_minor_updates
Revises: 0055_service_whitelist
Create Date: 2016-10-04 09:43:42.321138

"""

# revision identifiers, used by Alembic.
revision = '0056_minor_updates'
down_revision = '0055_service_whitelist'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('service_whitelist', 'recipient',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('services', 'research_mode',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('services_history', 'research_mode',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('templates', 'version',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key('templates_history_service_id_fkey', 'templates_history', 'services', ['service_id'], ['id'])
    op.create_foreign_key('templates_history_created_by_id_fkey', 'templates_history', 'users', ['created_by_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('templates_history_service_id_fkey', 'templates_history', type_='foreignkey')
    op.drop_constraint('templates_history_created_by_id_fkey', 'templates_history', type_='foreignkey')
    op.alter_column('templates', 'version',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('services_history', 'research_mode',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('services', 'research_mode',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('service_whitelist', 'recipient',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    ### end Alembic commands ###
