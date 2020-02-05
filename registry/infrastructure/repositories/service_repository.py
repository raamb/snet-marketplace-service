from datetime import datetime as dt
from registry.domain.factory.service_factory import ServiceFactory
from registry.infrastructure.models.models import Service, ServiceGroup, ServiceState, ServiceReviewHistory
from registry.infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy import func


class ServiceRepository(BaseRepository):
    def get_services_for_organization(self, org_uuid, payload):
        raw_services_data = self.session.query(Service). \
            filter(getattr(Service, payload["search_attribute"]).like("%" + payload["search_string"] + "%")). \
            filter(Service.org_uuid == org_uuid). \
            order_by(getattr(getattr(Service, payload["sort_by"]), payload["order_by"])()). \
            slice(payload["offset"], payload["limit"]).all()

        services = []
        for service in raw_services_data:
            services.append(ServiceFactory().convert_service_db_model_to_entity_model(service).to_dict())
        self.session.commit()
        return services

    def get_total_count_of_services_for_organization(self, org_uuid, payload):
        total_count_of_services = self.session.query(func.count(Service.uuid)). \
            filter(getattr(Service, payload["search_attribute"]).like("%" + payload["search_string"] + "%")). \
            filter(Service.org_uuid == org_uuid).all()[0][0]
        self.session.commit()
        return total_count_of_services

    def check_service_id_within_organization(self, org_uuid, service_id):
        record_exist = self.session.query(func.count(Service.uuid)).filter(Service.org_uuid == org_uuid) \
            .filter(Service.service_id == service_id).all()[0][0]
        return record_exist

    def add_service(self, service):
        service_db_model = ServiceFactory().convert_service_entity_model_to_db_model(service)
        self.add_item(service_db_model)

    def save_service(self, username, service):
        service_record = self.session.query(Service).filter(Service.org_uuid == service.org_uuid).filter(
            Service.uuid == service.uuid).first()
        self.session.query(ServiceGroup).filter(ServiceGroup.org_uuid == service.org_uuid).filter(
            ServiceGroup.service_uuid == service.uuid).delete()
        service_group_db_model = [ServiceFactory().convert_entity_model_to_service_group_db_model(group) for group in
                                  service.groups]
        service_record.display_name = service.display_name
        service_record.service_id = service.service_id
        service_record.metadata_ipfs_hash = service.metadata_ipfs_hash
        service_record.proto = service.proto
        service_record.short_description = service.project_url
        service_record.description = service.description
        service_record.project_url = service.project_url
        service_record.assets = service.assets
        service_record.rating = service.assets
        service_record.ranking = service.ranking
        service_record.contributors = service.contributors
        service_record.updated_on = dt.utcnow()
        service_record.groups = service_group_db_model
        service_record.service_state.state = service.service_state.state
        service_record.service_state.transaction_hash = service.service_state.transaction_hash
        service_record.service_state.updated_by = username
        service_record.service_state.updated_on = dt.utcnow()
        service_entity_model = ServiceFactory().convert_service_db_model_to_entity_model(service_record)
        self.session.commit()
        return service_entity_model

    def get_service_for_given_service_uuid(self, org_uuid, service_uuid):
        service = self.session.query(Service).filter(Service.org_uuid == org_uuid).filter(
            Service.uuid == service_uuid).first()
        service_entity_model = ServiceFactory().convert_service_db_model_to_entity_model(service)
        return service_entity_model

