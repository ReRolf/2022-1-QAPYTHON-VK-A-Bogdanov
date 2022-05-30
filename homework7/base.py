from utils.data_gen import create_name, create_job


class MockBase:
    @staticmethod
    def create_user(connect):
        name = create_name()
        user_job = create_job()
        user = {'name': name, 'job': user_job}
        response = connect.post('/create_user', user)
        return [user, response]
