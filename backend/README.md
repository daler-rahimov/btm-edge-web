## Windows powershell PYTHONENV setup
```powerhsell
PS C:\Users\spearsc> $env:PYTHONPATH = "."
PS C:\Users\spearsc> Get-ChildItem Env:PYTHONPATH

<!-- This is for PostgresSQL you can run it with docker-compose -->
PS C:\Users\spearsc> $env:DATABASE_URL = "postgresql://btm_web:password@localhost:5432/btm_web"
```

### Arduino conf
BoudRate = 115200
Parity   = None
DataBits = 8
