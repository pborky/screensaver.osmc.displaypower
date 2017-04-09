import os, sys, subprocess
import xbmc, xbmcgui, xbmcaddon

__addon__    = sys.modules[ '__main__' ].__addon__
__addonid__  = sys.modules[ '__main__' ].__addonid__
__cwd__      = sys.modules[ '__main__' ].__cwd__
__skindir__  = xbmc.getSkinDir().decode('utf-8')
__skinhome__ = xbmc.translatePath( os.path.join( 'special://home/addons/', __skindir__, 'addon.xml' ).encode('utf-8') ).decode('utf-8')
__skinxbmc__ = xbmc.translatePath( os.path.join( 'special://xbmc/addons/', __skindir__, 'addon.xml' ).encode('utf-8') ).decode('utf-8')

class Screensaver(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        pass

    def onInit(self):
        self._is_powered = True
        self.Monitor = MyMonitor(action = self._power_on)
        self._power_toggle()

    def _power_on(self):
        self._power_toggle()
        self.close()

    def _power_toggle(self):
        if self._is_powered:
            cmd1 = ['echo', 'standby', '0'] 
        else:
            cmd1 = ['echo', 'on', '0'] 
        try:
            cmd2 = ['/usr/osmc/bin/cec-client', '-d', '1', '-s']
            ps1 = subprocess.Popen((cmd1), stdout=subprocess.PIPE)
            ps2 = subprocess.Popen((cmd2), stdin=ps1.stdout, stdout=subprocess.PIPE)
            (out, err) = ps2.communicate()
            xbmc.log(msg="%s: cec-client returned %s" % ( __addonid__, repr(out) ), level=xbmc.LOGDEBUG)
            if not err:
                self._is_powered = not self._is_powered
            else:
                xbmc.log(msg="%s: cec-client returned %s" % ( __addonid__, repr(err) ), level=xbmc.LOGERROR)
        except:
            xbmc.log(msg="%s: Exception running cec-client" % ( __addonid__ ), level=xbmc.LOGERROR)


class MyMonitor(xbmc.Monitor):
    def __init__( self, *args, **kwargs ):
        self.action = kwargs['action']

    def onScreensaverDeactivated(self):
        self.action()

