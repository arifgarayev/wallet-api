from django.db import migrations

CREATE_SEQUENCE_RAW_SQL_QUERY = """
    CREATE SEQUENCE point_of_sale_seq
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        NO MAXVALUE
    CACHE 1;
"""

APPLY_SEQUENCE_RAW_SQL_QUERY = """
    ALTER TABLE core_pointofsale 
    ALTER COLUMN "id"
    SET DEFAULT nextval('point_of_sale_seq'::regclass);
"""


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial")
    ]

    operations = [
        # create sequence
        migrations.RunSQL(
            sql=CREATE_SEQUENCE_RAW_SQL_QUERY
        ),
        # apply to column
        migrations.RunSQL(
            sql=APPLY_SEQUENCE_RAW_SQL_QUERY
        ),
    ]
