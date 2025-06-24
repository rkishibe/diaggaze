# DiagGaze: Diagnosticarea autismului pe baza mișcărilor oculare 

## Adresa repository

Codul sursă complet al acestui proiect este disponibil la:

```
https://github.com/rkishibe/diaggaze
```

---
## Cerințe minime: Python 3+ instalat pe dispozitiv


## Pași de compilare

### 1. Clonare repository

```bash
git clone https://github.com/rkishibe/diaggaze.git
cd diaggaze/autism/asd
```

### 2. Backend (mongoDB)

1. Creare mediu virtual și activare:

   ```bash
   python -m venv venv
   venv\\Scripts\\activate
   ```
2. Instalare dependințe:

   ```bash
   pip install -r requirements.txt
   ```

3. MongoDB rulează (local sau remote)

4. Configurează variabilele de mediu, fie într-un .env, fie exportate manual:

    MONGO_URI – exemplu: mongodb://localhost:27017/heart_app

    SECRET_KEY – poate fi generat cu:
```bash
openssl rand -hex 32 > secret.key
set SECRET_KEY=$(< secret.key)
```
---

## Pași de instalare și lansare a aplicației

1. **Precondiții**
   * Fișierul "secret.key" este plasat în directorul rădăcină

2. **Lansarea aplicației**

   ```bash
	python app.py
