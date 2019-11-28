SC2 Api Emulator
================

SC2 client api emulator for testing purposes 

Run:
`docker pull leigholiver/sc2api`
`docker run -d --rm -p6120:80 --name sc2api leigholiver/sc2api`

Point your browser at `http://localhost:6120/` to configure the API responses 

You can then use the `http://localhost:6120/ui` and `http://localhost:6120/game` endpoints as if it were the SC2 API