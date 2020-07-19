import os
import unittest

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Asset, Inventory, Location, Ticket, TicketType


class TestBase(TestCase):

    def create_app(self):

        # pass in test configuration
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://fc_admin:fc_admin@localhost/fc_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        user = User(name="Rohit", password="admin2020",position="Stuccan",department="controls")


        # save users to database
        db.session.add(user)
        db.session.commit()
        #create static data
        if User.query.count()==1:
            user_id = user.id
            location = Location(description="ABQ-First")
            db.session.add(location)
            db.session.commit()
            inventory = Inventory(inventory_type="Fist Inv",purchased_by=user_id,location=location.id)
            db.session.add(inventory)
            db.session.commit()
            ticket_types = TicketType(description="First ticket_type")
            db.session.add(ticket_types)
            db.session.commit()
            ticket = Ticket(ticket_type=ticket_types.id,opened_by=user_id,updated_by=user_id,description="First Ticket")
            db.session.add(ticket)
            db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all() 
              
 
class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(User.query.count(), 1)


    def test_asset_model(self):
        """
        Test number of records in asssets table
        """

        # create test department
        asset = Asset(comments="test comments for asset",
            inventory_id=Inventory.query.first().id,
            location=Location.query.first().id,
            managed_by=User.query.first().id,
            assigned_to=User.query.first().id,
            certified_by=User.query.first().id,
             )

        # save department to database
        db.session.add(asset)
        db.session.commit()

        self.assertEqual(Asset.query.count(), 1)

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_assets_view(self):
        """
        Test that departments page is inaccessible without login
        and redirects to login page then to departments page
        """
        target_url = url_for('assets.list_assets')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
   