# Merge de `eliminar-paginas-modelo-viejo` a `main`

## Instrucciones para Abdelaziz

Ejecutar en orden en el terminal local:

```bash
# 1. Cambiar a main y asegurar que esta actualizado
git checkout main
git pull origin main

# 2. Merge de la rama de eliminacion
git merge eliminar-paginas-modelo-viejo

# 3. Push a produccion
git push origin main
```

## Post-deploy en EasyPanel

1. Entrar en EasyPanel
2. Pulsar **Deploy** en el servicio Certilab
3. Esperar 2-5 minutos a que el build termine
4. Verificar en ventana de incognito que las URLs viejas redirigen correctamente

## Checklist de verificacion post-deploy

- [ ] `https://certilab.cat/certificado-energetico/` -> redirige a `/por-que-no-emite-ce/`
- [ ] `https://certilab.cat/auditoria-energetica-online/` -> redirige a `/informe-tecnico-energetico/`
- [ ] `https://certilab.cat/obtener-certificado-energetico-gratis/` -> redirige a `/por-que-no-emite-ce/`
- [ ] `https://certilab.cat/precio-certificado-energetico/` -> redirige a `/por-que-no-emite-ce/`
- [ ] `https://certilab.cat/fondos-next-generation-2026/` -> redirige correctamente
- [ ] `https://certilab.cat/Tuexpedienteenergético/` -> redirige a `/expediente/`
- [ ] `https://certilab.cat/certificadoenergeticoinflado/` -> redirige a `/segunda-opinion/`

## Resumen del commit

| Commit | SHA | Mensaje |
|---|---|---|
| eliminacion | `5e73475` | chore: eliminar carpetas modelo viejo para activar redirects 301 |

**7 archivos eliminados** (2352 lineas):
- certificado-energetico/index.html
- auditoria-energetica-online/index.html
- obtener-certificado-energetico-gratis/index.html
- precio-certificado-energetico/index.html
- fondos-next-generation-2026/index.html
- Tuexpedienteenergético/index.html
- certificadoenergeticoinflado/index.html