import argparse
import nbformat
import pkg_resources

# reading the notebook content
def read_notebook_content(notebook_path):
    with open(notebook_path, 'r') as file:
        notebook_content = nbformat.read(file, as_version=4)
    return notebook_content


def generate_reqs_txt(ipynb_path):
    ntbk_content = read_notebook_content(ipynb_path)
    libs_versions = {}
    #NOTE: Extremely inefficient but ast did not work when i tried to use it to parse the ntbk so sticking to nbformat 
    for cell in ntbk_content.cells:
        if cell.cell_type == 'code':
            for line in cell.source.split('\n'):
                if line.startswith('import') or line.startswith('from'):
                    lib = line.split()[1]
                    try:
                        #getting the version numbers for the libraries found 
                        version = pkg_resources.get_distribution(lib).version
                    except pkg_resources.DistributionNotFound:
                        #add library without version 
                        version = None
                    libs_versions[lib] = version
                        

    with open("requirements.txt", "w") as req_file:
        #save library with the version
        #NOTE: THIS DOES NOT GURANTEE THAT THERE WILL BE NO VERSION CONFLICTS(next update will be trying to use uv to fix)
        print(libs_versions)
        for lib, ver in libs_versions.items():
            if ver:
                req_file.write(f"{lib}=={ver}\n")
            else: 
                req_file.write(f"{lib}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ipynb_path", help="Path to the Jupyter Notebook")
    args = parser.parse_args()

    generate_reqs_txt(args.ipynb_path)
