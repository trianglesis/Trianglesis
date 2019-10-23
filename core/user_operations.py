"""
Check user models, names, groups.

"""
# Python logger
import logging

log = logging.getLogger("core.corelogger")


class UserCheck:

    @staticmethod
    def get_user_name(request):
        user_name = request.user.get_username()
        if not user_name:
            user_name = "Anonymous"
        return user_name

    @staticmethod
    def is_member(user, group):
        if user and group:
            return user.groups.filter(name=group).exists()
        else:
            return False

    @staticmethod
    def is_staff(user):
        return user.groups.filter(name='admin_users').exists()

    @staticmethod
    def is_power(user):
        return user.groups.filter(name='power_users').exists()

    def user_string_f(self, request):
        user_name = self.get_user_name(request)
        user_addr = request.META['REMOTE_ADDR']
        user_string = "User: '{0}' IP: {1}".format(user_name, user_addr)
        return user_name, user_string
