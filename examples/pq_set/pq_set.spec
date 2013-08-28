# -*- mode: python -*-
a = Analysis(['pq_set.py'],
             pathex=[],
             hiddenimports=[],
             hookspath=None)
a.datas += [('ca.ico', 'ca.ico',  'DATA'), ('pq_set.yaml', 'pq_set.yaml',  'DATA'),]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'pq_set.exe'),
          debug=False,
          strip=None,
          upx=True,
          icon='ca.ico',
          console=False)
