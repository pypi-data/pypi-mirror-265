import chainlo.agenta_cli.agenta
import _app
from mangum import Mangum


handler = Mangum(agenta.app)
