from uuid import uuid4

from database.database_setup import db
from database.models import CountryTable, InfoPageTable, UniversityTable
from flask_restful import Resource, abort, marshal_with, reqparse
from resources_api.resource_fields_definitions import (
    search_universities_resource_fields,
    university_meta_table_resource_fields,
    university_resource_fields,
    university_with_info_resource_fields,
)
from sqlalchemy import exc, select


class UniversityRes(Resource):
    @marshal_with(university_resource_fields)
    def get(self, university_id):
        stmt = (
            select(UniversityTable, CountryTable)
            .join(
                CountryTable,
                UniversityTable.country_code == CountryTable.country_code,
            )
            .where(UniversityTable.university_id == university_id)
        )
        res = db.session.execute(stmt).first()

        # None can happens if UniversityTable.country_code is null
        if res is None:
            result = db.get_or_404(
                UniversityTable,
                university_id,
                description=f"No univerisity with the ID '{university_id}'.",
            )
        else:
            parent, child = res
            result = parent.__dict__
            result.update(child.__dict__)
        return result, 200


class UniversityWithInfoRes(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument(
            "university_id", type=str, location="args", required=True
        )

        self.post_args = reqparse.RequestParser()
        self.post_args.add_argument(
            "university_id", type=str, location="args", required=True
        )
        self.post_args.add_argument(
            "webpage", type=str, location="args", help="Webpage to create info"
        )
        self.post_args.add_argument(
            "introduction",
            type=str,
            location="args",
            help="Introduction to create info",
        )
        self.post_args.add_argument(
            "location", type=str, location="args", help="location to create info"
        )
        self.post_args.add_argument(
            "semester", type=str, location="args", help="semester to create info"
        )
        self.post_args.add_argument(
            "application_deadlines",
            type=str,
            location="args",
            help="Application deadlines to create info",
        )
        self.post_args.add_argument(
            "courses", type=str, location="args", help="courses to create info"
        )
        self.post_args.add_argument(
            "housing", type=str, location="args", help="housing to create info"
        )
        self.post_args.add_argument(
            "expenses", type=str, location="args", help="expenses to create info"
        )
        self.post_args.add_argument(
            "visa", type=str, location="args", help="visa to create info"
        )
        self.post_args.add_argument(
            "eligibility", type=str, location="args", help="eligibility to create info"
        )
        self.post_args.add_argument(
            "requirements",
            type=str,
            location="args",
            help="requirements to create info",
        )
        self.post_args.add_argument("additional_information", type=str, location="args")

        self.patch_args = reqparse.RequestParser()
        self.patch_args.add_argument(
            "info_page_id",
            type=str,
            location="args",
            required=True,
            help="Info page ID to update info",
        )
        self.patch_args.add_argument(
            "webpage", type=str, location="args", help="Webpage to create info"
        )
        self.patch_args.add_argument(
            "introduction",
            type=str,
            location="args",
            help="Introduction to create info",
        )
        self.patch_args.add_argument(
            "location", type=str, location="args", help="location to create info"
        )
        self.patch_args.add_argument(
            "semester", type=str, location="args", help="semester to create info"
        )
        self.patch_args.add_argument(
            "application_deadlines",
            type=str,
            location="args",
            help="Application deadlines to create info",
        )
        self.patch_args.add_argument(
            "courses", type=str, location="args", help="courses to create info"
        )
        self.patch_args.add_argument(
            "housing", type=str, location="args", help="housing to create info"
        )
        self.patch_args.add_argument(
            "expenses", type=str, location="args", help="expenses to create info"
        )
        self.patch_args.add_argument(
            "visa", type=str, location="args", help="visa to create info"
        )
        self.patch_args.add_argument(
            "eligibility", type=str, location="args", help="eligibility to create info"
        )
        self.patch_args.add_argument(
            "requirements",
            type=str,
            location="args",
            help="requirements to create info",
        )
        self.patch_args.add_argument(
            "additional_information", type=str, location="args"
        )

    @marshal_with(university_with_info_resource_fields)
    def get(self):
        args = self.get_args.parse_args()
        university_id = args["university_id"]

        uni = db.get_or_404(
            UniversityTable,
            university_id,
            description=f"No Univerisity with the ID '{university_id}'.",
        )

        return db.get_or_404(
            InfoPageTable,
            uni.info_page_id,
            description=f"No university with the ID '{university_id}'.",
        )

    @marshal_with(university_with_info_resource_fields)
    def post(self):
        try:
            args = self.post_args.parse_args()
            university_id = args["university_id"]

            uni = db.get_or_404(
                UniversityTable,
                university_id,
                description=f"No Univerisity with the ID '{university_id}'.",
            )
            if uni.info_page_id is not None:
                abort(
                    message="Information page already existed with provided university_id, use PATCH instead",
                    http_status_code=400,
                )

            new = InfoPageTable(
                info_page_id=str(uuid4()),
                webpage=args["webpage"],
                introduction=args["introduction"],
                location=args["location"],
                semester=args["semester"],
                application_deadlines=args["application_deadlines"],
                courses=args["courses"],
                housing=args["housing"],
                expenses=args["expenses"],
                visa=args["visa"],
                eligibility=args["eligibility"],
                requirements=args["requirements"],
                additional_information=args["additional_information"],
            )

            db.session.add(new)
            db.session.commit()

            uni.info_page_id = new.info_page_id
            db.session.commit()

            return new, 200
        except exc.SQLAlchemyError as e:
            print(e)
            abort(message=str(e.__dict__.get("orig")), http_status_code=400)

    @marshal_with(university_with_info_resource_fields)
    def patch(self):
        try:
            args = self.patch_args.parse_args()
            info_page_id = args["info_page_id"]
            info_page = db.get_or_404(
                InfoPageTable,
                info_page_id,
                description=f"No InfoPage with the ID '{info_page_id}'.",
            )

            if "webpage" in args and args["webpage"] is not None:
                info_page.webpage = args["webpage"]
            if "introduction" in args and args["introduction"] is not None:
                info_page.introduction = args["introduction"]
            if "location" in args and args["location"] is not None:
                info_page.location = args["location"]
            if "semester" in args and args["semester"] is not None:
                info_page.semester = args["semester"]
            if (
                "application_deadlines" in args
                and args["application_deadlines"] is not None
            ):
                info_page.application_deadlines = args["application_deadlines"]
            if "courses" in args and args["courses"] is not None:
                info_page.courses = args["courses"]
            if "housing" in args and args["housing"] is not None:
                info_page.housing = args["housing"]
            if "expenses" in args and args["expenses"] is not None:
                info_page.expenses = args["expenses"]
            if "visa" in args and args["visa"] is not None:
                info_page.visa = args["visa"]
            if "eligibility" in args and args["eligibility"] is not None:
                info_page.eligibility = args["eligibility"]
            if "requirements" in args and args["requirements"] is not None:
                info_page.requirements = args["requirements"]
            if (
                "additional_information" in args
                and args["additional_information"] is not None
            ):
                info_page.additional_information = args["additional_information"]

            db.session.commit()

            return info_page, 200

        except exc.SQLAlchemyError as e:
            print(e)
            abort(message=str(e.__dict__.get("orig")), http_status_code=400)


class UniversityAllRes(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.put_args = reqparse.RequestParser()
        self.put_args.add_argument(
            "university_id",
            type=str,
            location="args",
            help="University ID to create university",
        )
        self.put_args.add_argument(
            "country_code", type=str, location="args", help="Uni country code"
        )
        self.put_args.add_argument(
            "region", type=str, location="args", help="Uni region"
        )
        self.put_args.add_argument(
            "long_name", type=str, location="args", help="Full name of university"
        )
        self.put_args.add_argument(
            "ranking", type=str, location="args", help="Ranking of a university"
        )
        self.put_args.add_argument(
            "info_page_id",
            type=str,
            location="args",
            help="Information of a university",
        )
        self.put_args.add_argument(
            "campus", type=str, location="args", help="Campus of a university"
        )
        self.put_args.add_argument(
            "housing",
            type=str,
            location="args",
            help="Housing availability of a university",
        )

        self.update_args = reqparse.RequestParser()
        self.update_args.add_argument(
            "university_id",
            type=str,
            location="args",
            help="University ID to create university",
        )
        self.update_args.add_argument(
            "country_code", type=str, location="args", help="Uni country code"
        )
        self.update_args.add_argument(
            "region", type=str, location="args", help="Uni region"
        )
        self.update_args.add_argument(
            "long_name", type=str, location="args", help="Full name of university"
        )
        self.update_args.add_argument(
            "ranking", type=str, location="args", help="Ranking of a university"
        )
        self.update_args.add_argument(
            "info_page_id",
            type=str,
            location="args",
            help="Information of a university",
        )
        self.update_args.add_argument(
            "campus", type=str, location="args", help="Campus of a university"
        )
        self.update_args.add_argument(
            "housing",
            type=str,
            location="args",
            help="Housing availability of a university",
        )

        self.delete_args = reqparse.RequestParser()
        self.delete_args.add_argument(
            "university_id",
            type=str,
            location="args",
            help="Uni ID to delete university",
        )

    @marshal_with(university_meta_table_resource_fields)
    def get(self):
        unis = UniversityTable.query.order_by(UniversityTable.long_name).all()
        return [uni for uni in unis], 200
        # return universities_schema.dump(unis)

    @marshal_with(university_meta_table_resource_fields)
    def post(self):
        try:
            args = self.put_args.parse_args()

            new_uni = UniversityTable(
                university_id=str(uuid4()),
                country_code=args["country_code"],
                region=args["region"] if args["region"] != "" else None,
                long_name=args["long_name"],
                ranking=args["ranking"] if args["ranking"] != "" else None,
                info_page_id=args["info_page_id"],
                campus=args["campus"] if args["campus"] != "" else None,
                housing=args["housing"],
            )

            new_info = InfoPageTable(
                info_page_id=str(uuid4()),
                webpage="https://example.com/",
            )

            new_uni.info_page_id = new_info.info_page_id

            db.session.add(new_uni)
            db.session.add(new_info)
            db.session.commit()
            return new_uni, 200
        except exc.SQLAlchemyError as e:
            print(e)
            abort(message=str(e.__dict__.get("orig")), http_status_code=400)

    @marshal_with(university_meta_table_resource_fields)
    def patch(self):
        try:
            args = self.update_args.parse_args()
            uniid = args["university_id"]
            uni = (
                db.session.query(UniversityTable).filter_by(university_id=uniid).first()
            )

            if "country_code" in args and args["country_code"] is not None:
                uni.country_code = (
                    args["country_code"] if args["country_code"] != "" else None
                )
            if "region" in args and args["region"] is not None:
                uni.region = args["region"] if args["region"] else None
            if "long_name" in args and args["long_name"] is not None:
                uni.long_name = args["long_name"] if args["long_name"] else None
            if "ranking" in args and args["ranking"] is not None:
                uni.ranking = args["ranking"] if args["ranking"] else None
            if "info_page_id" in args and args["info_page_id"] is not None:
                uni.info_page_id = (
                    args["info_page_id"] if args["info_page_id"] else None
                )
            if "campus" in args and args["campus"] is not None:
                uni.campus = args["campus"] if args["campus"] else None
            if "housing" in args and args["housing"] is not None:
                uni.housing = args["housing"] if args["housing"] else "N/A"

            db.session.commit()

            return uni, 200

        except exc.SQLAlchemyError as e:
            print(e)
            abort(message=str(e.__dict__.get("orig")), http_status_code=400)

    def delete(self):
        try:
            args = self.delete_args.parse_args()
            university_id = args["university_id"]
            uni = db.get_or_404(
                UniversityTable,
                university_id,
                description=f"No Univerisity with the ID '{university_id}'.",
            )
            db.session.delete(uni)
            db.session.commit()
            print(f"University with uni_id '{university_id}' deleted successfully")
            return {
                "message": f"University with uni_id '{university_id}' deleted successfully"
            }, 200
        except Exception as e:
            print(f"An error occurred: {e}")
            abort(message=str(e), http_status_code=500)


class UniversityPagination(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "page_number", type=int, default=1, location="args", required=True
        )
        self.reqparse.add_argument(
            "search_word", type=str, default="", location="args", required=True
        )

    # pagination: https://www.youtube.com/watch?v=hkL9pgCJPNk
    @marshal_with(search_universities_resource_fields)
    def get(self):
        args = self.reqparse.parse_args()
        page_number = args["page_number"]
        search_word = args["search_word"]

        if search_word == "":
            res = db.paginate(select(UniversityTable), per_page=10, page=page_number)
        else:
            res = db.paginate(
                select(UniversityTable).where(
                    UniversityTable.long_name.contains(search_word)
                ),
                per_page=10,
                page=page_number,
            )
        return {"hasMore": res.has_next, "items": [r for r in res]}, 200
