from unittest import TestCase
import sqlite3
from tempfile import gettempdir
import os
import shutil
import platform
from time import sleep
from aequilibrae.project.network.network import Network
from aequilibrae.parameters import Parameters
from aequilibrae.reference_files import spatialite_database


class TestNetwork(TestCase):
    def setUp(self) -> None:
        self.file = os.path.join(gettempdir(), "aequilibrae_project_test.sqlite")
        shutil.copyfile(spatialite_database, self.file)
        self.conn = sqlite3.connect(self.file)
        self.conn.enable_load_extension(True)
        plat = platform.platform()
        pth = os.getcwd()
        if "WINDOWS" in plat.upper():
            par = Parameters()
            spatialite_path = par.parameters["system"]["spatialite_path"]
            if os.path.isfile(os.path.join(spatialite_path, "mod_spatialite.dll")):
                os.chdir(spatialite_path)
        self.conn.load_extension("mod_spatialite")
        os.chdir(pth)

        # cur = self.conn.cursor()
        # sql = """CREATE TABLE 'links' (
        #           ogc_fid INTEGER PRIMARY KEY, -- Hidden widget
        #           link_id INTEGER UNIQUE NOT NULL, -- Text edit widget with 'Not null' constraint
        #           a_node INTEGER, -- Text edit widget, with 'editable' unchecked
        #           b_node INTEGER, -- Text edit widget, with 'editable' unchecked
        #           direction INTEGER, -- Range widget, 'Editable', min=0, max=2, step=1, default=0
        #           capacity_ab REAL,
        #           capacity_ba REAL,
        #           lanes_ab INTEGER,
        #           lanes_ba INTEGER,
        #           speed_ab REAL,
        #           speed_ba REAL,
        #           'length' REAL,
        #           osm_id INTEGER,
        #           name VARCHAR,
        #           link_type VARCHAR
        #         );
        #         #
        #         SELECT AddGeometryColumn( 'links', 'geometry', 4326, 'LINESTRING', 'XY' );
        #         #
        #         CREATE TABLE 'nodes' (
        #           ogc_fid INTEGER PRIMARY KEY,
        #           node_id INTEGER UNIQUE NOT NULL,
        #           osm_id INTEGER,
        #           is_centroid INTEGER
        #         );
        #         #
        #         SELECT AddGeometryColumn( 'nodes', 'geometry', 4326, 'POINT', 'XY' );
        #         """
        # for sql_sta in sql.split("#"):
        #     cur.execute(sql_sta)
        # self.conn.commit()
        self.network = Network(self)

    def tearDown(self) -> None:
        self.conn.close()
        os.unlink(self.file)

    def test_create_from_osm(self):
        self.network.create_from_osm(west=-112.185, south=36.59, east=-112.179, north=36.60, modes=["car"])

        curr = self.conn.cursor()

        curr.execute("""select count(*) from links""")
        lks = curr.fetchone()

        curr.execute("""select count(distinct osm_id) from links""")
        osmids = curr.fetchone()

        if osmids >= lks:
            self.fail("OSM links not broken down properly")

        curr.execute("""select count(*) from nodes""")
        nds = curr.fetchone()

        if lks > nds:
            self.fail("We imported more links than nodes. Something wrong here")

    def test_count_links(self):
        self.fail()

    def test_count_nodes(self):
        self.fail()
