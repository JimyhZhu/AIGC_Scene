import asyncio
import typer
from metagpt.logs import logger
from metagpt.team import Team
from Roles import *

app = typer.Typer()


@app.command()
def main(
    object_type: str = typer.Argument(default="cube", help="Type of object to add (cube, circle, uv_sphere)"),
    location: str = typer.Argument(default="0,0,0", help="Location to place the object, format: 'x,y,z'"),
    investment: float = typer.Option(default=3.0, help="Dollar amount to invest in the AI company."),
    n_round: int = typer.Option(default=5, help="Number of rounds for the simulation."),
):
    logger.info(f"Adding {object_type} at location {location}")

    # Convert location string to tuple
    location_tuple = tuple(map(float, location.split(',')))

    team = Team()
    team.hire(
        [
            BlenderOperator(),
            SceneVerifier(),
        ]
    )

    team.invest(investment=investment)
    
    # Run project to add the object
    team.run_project((object_type, location_tuple))

    # Verify the scene
    team.run_project(None, task_class=VerifyBlenderScene)
    
    asyncio.run(team.run(n_round=n_round))

if __name__ == '__main__':
    app()