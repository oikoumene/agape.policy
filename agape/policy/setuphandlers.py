from collective.grok import gs
from agape.policy import MessageFactory as _

@gs.importstep(
    name=u'agape.policy', 
    title=_('agape.policy import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('agape.policy.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
