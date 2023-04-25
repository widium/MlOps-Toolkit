# *************************************************************************** #
#                                                                              #
#    hugging_face.py                                                           #
#                                                                              #
#    By: Widium <ebennace@student.42lausanne.ch>                               #
#    Github : https://github.com/widium                                        #
#                                                                              #
#    Created: 2023/04/25 07:48:31 by Widium                                    #
#    Updated: 2023/04/25 07:48:31 by Widium                                    #
#                                                                              #
# **************************************************************************** #

from pathlib import Path
from huggingface_hub import HfApi, Repository, create_repo

class HuggingFaceRepositoryCreator:
    """
    Create Hugging Face repository in hub
    Clone inside local folder
    Setup it with basic file structure
    Push it to hugging face hub 
    
    Initialize Creator with write token
    """
    def __init__(self, api_token: str):
        """
        Initialize HuggingFaceRepositoryCreator with an API token.
        
        Args:
            api_token (str): Hugging Face API token
        """
        self.api = HfApi()
        self.api_token = api_token
    
    def create_repository_on_hub(
        self, 
        repo_name : str,
        repo_type : str = "space",
        space_sdk : str = "gradio",
        space_hardware : str = "cpu-basic",
        private: bool = False,
        destination : str = "."
    )->None:
        """
        Create a repository on Hugging Face Hub with the given parameters.
        
        Args:
            repo_name (str): Repository name
            repo_type (str, optional): Repository type. Defaults to "space".
            space_sdk (str, optional): Space SDK. Defaults to "gradio".
            space_hardware (str, optional): Space hardware. Defaults to "cpu-basic".
            private (bool, optional): Set repository private or public. Defaults to False.
            destination (str, optional): Destination folder. Defaults to ".".
        """
        
        self.user = self.api.whoami(token=self.api_token)
        print(f"[INFO] : Successfully Logged in Hugging Face Hub.") 
        self.namespace = self.user['name']
        self.repo_full_name = f"{self.namespace}/{repo_name}"
        self.destination_path = Path(destination) / repo_name
        
        self.repo_url = create_repo(
            repo_id=self.repo_full_name,
            token=self.api_token,
            repo_type=repo_type,
            space_sdk=space_sdk,
            space_hardware=space_hardware,
            private=private,
            exist_ok=True,
        )
        print(f"[INFO] : Repository Successfully Created in Hugging Face Hub [{self.repo_url}].") 
        
    def clone_repository(self, repo_url : str, api_token : str, destination_path : Path)->None:
        """
        Clone the repository from the given URL to the destination path.
        
        Args:
            repo_url (str): Repository URL
            api_token (str): Hugging Face API token
            destination_path (Path): Destination path for the cloned repository
        """
        self.repository = Repository(
            local_dir=destination_path,
            clone_from=repo_url,
            use_auth_token=api_token
        )
        
        print(f"[INFO] : Repository Successfully Cloned in [{destination_path}].")
        
    def setup_repository(self, path : str):
        """
        Set up the repository with initial files and folder structure.
        
        Args:
            path (str): Path to the repository folder
        """
        root = Path(path)
        app_path = root / "app.py"
        requirement_path = root / "requirements.txt"
        readme_path = root / "README.md"
        examples_path = root / "examples"
        
        app_path.touch()
        requirement_path.touch()
        examples_path.mkdir(parents=True, exist_ok=True)
        
        with app_path.open("w") as file :
            app_content = "import gradio as gr\n"
            app_content += "\ndef greet(name):\n"
            app_content += "    return 'Hello ' + name + '!!'\n"
            app_content += "iface = gr.Interface(fn=greet, inputs='text', outputs='text')\n"
            app_content += "iface.launch()\n"
        
            file.write(app_content)
        
        print(f"[INFO] : create [{app_path} 'with content', {requirement_path}, {readme_path}, {examples_path}].")
        
        self.repository.git_add()
        self.repository.git_commit(commit_message="Initialize Repository App")
        self.repository.git_push()
        
        print(f"[INFO] : First Commit Successfully Initialized.")      
        
    def create_repository(
        self, 
        repo_name : str,
        repo_type : str = "space",
        space_sdk : str = "gradio",
        space_hardware : str = "cpu-basic",
        private: bool = False,
        destination : str = "."
    ) -> Repository:
        """
        Create a repository on Hugging Face Hub, clone it locally, and set up the initial structure.
        
        Args:
            repo_name (str): Repository name
            repo_type (str, optional): Repository type. Defaults to "space".
            space_sdk (str, optional): Space SDK. Defaults to "gradio".
            space_hardware (str, optional): Space hardware. Defaults to "cpu-basic".
            private (bool, optional): Set repository private or public. Defaults to False.
            destination (str, optional): Destination folder. Defaults to ".".
        
        Returns:
            Repository: Created repository object
        """
        self.create_repository_on_hub(
            repo_name=repo_name,
            repo_type=repo_type,
            space_sdk=space_sdk,
            space_hardware=space_hardware,
            private=private,
            destination=destination,
        )
        
        self.clone_repository(
            repo_url=self.repo_url, 
            api_token=self.api_token, 
            destination_path=self.destination_path
        )
        
        self.setup_repository(path=self.destination_path)
        
        return (self.repository)