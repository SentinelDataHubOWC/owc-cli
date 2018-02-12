import click
import os
import json
import git


class GitRepository:
    name = ""
    version = ""

    def __init__(self, name="", version=""):
        self.name = name
        self.version = version

OWC_COMPONENT_GITHUB = "https://github.com/SentinelDataHubOWCElements/"
BOWER_COMPONENTS_FOLDER = "/bower_components/"

@click.group()
def cli():

    pass

# @cli.command()
# def init():
#     """Setup development environment """
#     click.echo('Initial ')


@cli.command()
def about():
    """Information about OWCLI."""
    click.echo("""
        _____      _____     ___ _    ___
       / _ \ \    / / __|__ / __| |  |_ _|
      | (_) \ \/\/ / (_|___| (__| |__ | |
       \___/ \_/\_/ \___|   \___|____|___|

    """)

    click.echo("""
               _-o#&&*''''?d:>b\_
          _o/\"`''  '',, dMF9MMMMMHo_
       .o&#'        `\"MbHMMMMMMMMMMMHo.
     .o\"\" '         vodM*$&&HMMMMMMMMMM?.
    ,'              $M&ood,~'`(&##MMMMMMH\\
   /               ,MMMMMMM#b?#bobMMMMHMMML
  &              ?MMMMMMMMMMMMMMMMM7MMM$R*Hk
 ?$.            :MMMMMMMMMMMMMMMMMMM/HMMM|`*L
|               |MMMMMMMMMMMMMMMMMMMMbMH'   T,
$H#:            `*MMMMMMMMMMMMMMMMMMMMb#}'  `?
]MMH#             \"\"*\"\"\"\"*#MMMMMMMMMMMMM'    -
MMMMMb_                   |MMMMMMMMMMMP'     :
HMMMMMMMHo                 `MMMMMMMMMT       .
?MMMMMMMMP                  9MMMMMMMM}       -
-?MMMMMMM                  |MMMMMMMMM?,d-    '
 :|MMMMMM-                 `MMMMMMMT .M|.   :
  .9MMM[                    &MMMMM*' `'    .
   :9MMk                    `MMM#\"        -
     &M}                     `          .-
      `&.                             .
        `~,   .                     ./
            . _                  .-
              '`--._,dd###pp=\"\"'
    """)
    click.echo("OWCLI is the OWC command line interface tool to help the components developer and maintainer. ")
    click.echo("Please launch 'owcli --help' to show the help page.")
    click.echo("\n");


# bower install
@cli.command()
@click.option('--safe', is_flag=True, default=True,  help='Executes the task without overriding the bower dependencies using bower install command. Default=true.')
@click.option('--clone', default="", help="Contains the list of owc components to clone, replacing the bower components dowloaded using bower install command. The syntax is: <owc-component-name-1>,<owc-component-name-2>. Default=\"\".")
@click.option('--dev', is_flag=True, default=True,  help="Download dev dependencies via bower, defined in bower.json file. Default=true.")
@click.option('--clone-all', default=False, is_flag=True, help="Clone all owc components present in bower_components folder, with checkout in master branch. Default=false.")
@click.option('--clear', default=False, is_flag=True, help="Before to run the task, remove bower_components folder. Default=false.")
@click.option('--repository-organization-url', default=OWC_COMPONENT_GITHUB, help="Repository organization url or git server user, where are located the components repositories. Default: " + OWC_COMPONENT_GITHUB)
def bower(safe,clone, dev, clone_all, clear, repository_organization_url):
    """This task manages the bower dependencies, providing the possibility to clone owc elements"""
    click.echo('[OWCLI] - BOWER TASK')

    if clear:
        click.echo('[OWCLI] - BOWER CLEAR')
        thedir = os.getcwd()  + BOWER_COMPONENTS_FOLDER
        if not thedir:
            click.echo("Error: cleaning this folder:  " + thedir + "? (⊙_☉) Please check your configurations." )
        else:
            click.echo("[OWCLI] - Cleaning the folder: " + thedir + " ٩ʕ•͡×•ʔ۶")
            os.system("rm -rf " + thedir )

    data = json.load(open('bower.json'))
    dependencies = data['dependencies']
    devdependencies =  data['devDependencies']
    click.echo("[OWCLI] - INSTALL  DEPENDENCIES")
    for key in data['dependencies']:
        dep = data['dependencies'][key]
        click.echo("dependency: " + dep)
        isOwcElement = key.startswith("owc-")
        if safe and isOwcElement:
            click.echo( dep + " is an owc component (SKIPPED)")
            pass
        else:
            click.echo("install dependency: " + dep)
            os.system("bower install " + dep)

    if dev:
        click.echo("[OWCLI] - INSTALL DEV DEPENDENCIES")
        for key in data['devDependencies']:
            devdep = data['devDependencies'][key]
            click.echo("install dev dependency: " + devdep)
            os.system("bower install " + devdep)
    if clone_all:
        click.echo("[OWCLI] - CLONE ALL OWC ELEMENTS")
        thedir = os.getcwd()  + BOWER_COMPONENTS_FOLDER
        components = [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        for component in components:

            if component.startswith("owc-"):
                click.echo(component)
                os.system("rm -rf " + thedir +  component)
                dep = None
                repo = repository_organization_url + component + ".git"
                git.Git(str(os.getcwd() + BOWER_COMPONENTS_FOLDER)).clone(repo)
    if clone:
        to_clone = []
        click.echo("[OWCLI] - CLONE " )
        if "," in clone:
            components = clone.split(",")

            for component in components:
                to_clone.append(GitRepository(component))
        else:
            to_clone.append(GitRepository(clone))

        for item in to_clone:
            if item.name.startswith("owc-"):
                thedir = os.getcwd()  + BOWER_COMPONENTS_FOLDER
                os.system("rm -rf " + thedir +  item.name)
                repo = repository_organization_url + item.name + ".git"
                cose = git.Git(str(os.getcwd() + BOWER_COMPONENTS_FOLDER)).clone(repo)
                click.echo("[OWCLI] - CLONED '" + repo + "' REPOSITORY. ʕ•̫͡•ʕ•̫͡•ʔ•̫͡•ʔ" )
            else:
                click.echo("Error: " + item.name + " is not an owc component. [SKIPPED]")
                pass
