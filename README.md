# recipe-planning-recipe-service
This is the repo for recipe CRUD service.

## Getting Started

1. Install [Docker](https://www.docker.com/get-started/)
2. Launch Docker
3. In the repo directory run the `./scripts/build.sh`


## Database versioning

Install alembic version found in requirements.txt. As of writing this 1.31.1. `pip3 install alembic==1.31.1`

When adding a new model with `Base`, be sure to import it to `alembic/env.py`.

When finished making changes to any Model run `alembic revision --autogenerate -m "Some desciption of db changes"`

A new migration script should appear in `alembic/versions/` check to see if the `upgrade` function makes sense (if a new column was added then `add_column` should have been called) and `downgrade` is logically the opposite of `upgrade`.

When finalized we can update the versioning of the database to the most recent changes. run `alembic upgrade head`.

If you want to undo the upgrade you can run `alembic downgrade -1`. Or specify which ever is the most recent version's `revision` hash. `-1` is a relative downgrade i.e. because we upgraded to head, if we want to undo it we downgrade by one version.
