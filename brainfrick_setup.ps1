if(-Not (Test-Path -path ".\img-brainfrickery")){
    python -m venv .\img-brainfrickery
    .\img-brainfrickery\Scripts\Activate.ps1
    python -m pip install -r .\requirements_windows.txt
}

if(-Not (Test-Path -path ".\setup.cfg")){
    "[build]`ncompiler=mingw32`n[build_ext]`ncompiler=mingw32" | Out-File -encoding ascii -FilePath .\setup.cfg
}

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    winget install --id=MSYS2.MSYS2  -e 
    C:\msys64\usr\bin\bash.exe -l -c "pacman -Syuu && pacman -S mingw-w64-x86_64-gcc"
}
else {
    Start-Process -Wait -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs
    $env:Path += ';C:\msys64\mingw64\bin;C:\msys64\usr\bin'
    python brainfrick_extension_build.py
}