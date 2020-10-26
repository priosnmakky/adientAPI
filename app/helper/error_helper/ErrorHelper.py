from truck_plan_management.models import PickUp

class ErrorHelper:

    @staticmethod
    def get_error_massage(errors_dist):

        return errors_dist[list(errors_dist)[0]][0]


