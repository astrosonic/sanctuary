# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files =[
    ('templates/', 'templates'),
    ('static/', 'static'),
    ('pictures/', 'pictures'),
    ]



a = Analysis(['servchat.py'],
             pathex=['/home/sara/personal/Hacktoberfest/sanctuary/sanctuary'],
             binaries=[],
             datas = added_files, # set datas = added_files list
             hiddenimports=['jinja2.ext'], # be sure to add jinja2 
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ChatRoom',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
