# -*- mode: python -*-
a = Analysis(['pyLogger.py'],
             pathex='',#['F:\\Bird\\bird\\BirdGui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='pyLogger.exe',
          debug=False,
          strip=None,
          upx=False,
          icon='pyLogger.ico',
          console=False)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='cli.exe',
          debug=False,
          strip=None,
          upx=False,
          icon='pyLogger.ico',
          console=True)

