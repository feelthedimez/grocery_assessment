from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver

logger = get_logger(logger_name=__name__)

@given(u'I just need to demo')
def step_impl(context):

    context.driver = initialize_driver()

    config_file = read_config_file(section='auth')
    username = config_file['username']
    password = config_file['password']

    data = AmplifyEcommerce(context.driver).login(username=username, password=password)