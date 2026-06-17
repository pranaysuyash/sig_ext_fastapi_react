import os
import shutil
import subprocess

def read_include_list(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

def prepare_deployment(include_list, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    for item in include_list:
        if os.path.exists(item):
            dest = os.path.join(output_dir, item)
            if os.path.isdir(item):
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        else:
            print(f"Warning: {item} not found.")

def deploy(output_dir):
    print(f"Deploying {output_dir} to Cloudflare Pages...")
    subprocess.run(["npx", "wrangler", "pages", "deploy", output_dir], check=True)

if __name__ == "__main__":
    include_file = ".pages-include"
    deploy_dir = "deploy_dist"
    
    if os.path.exists(include_file):
        print(f"Using {include_file} to prepare deployment...")
        items = read_include_list(include_file)
        prepare_deployment(items, deploy_dir)
        try:
            deploy(deploy_dir)
        except subprocess.CalledProcessError as e:
            print(f"Deployment failed: {e}")
        finally:
            # Optional: cleanup
            # shutil.rmtree(deploy_dir)
            print("Done.")
    else:
        print(f"{include_file} not found. Aborting.")
