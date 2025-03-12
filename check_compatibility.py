import pkg_resources

def check_installed_versions():
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    print("Installed packages:")
    for pkg_name in sorted(installed_packages.keys()):
        print(f"{pkg_name}=={installed_packages[pkg_name]}")
    
    print("\nChecking solana and solders compatibility...")
    solana_version = installed_packages.get('solana')
    solders_version = installed_packages.get('solders')
    
    if solana_version and solders_version:
        print(f"Found solana=={solana_version} and solders=={solders_version}")
        print("These versions are incompatible according to the error message.")
        print("Recommendation: Either downgrade solders to <0.15.0 or upgrade solana.")
    else:
        print("Could not find installed versions of solana and/or solders.")

if __name__ == "__main__":
    check_installed_versions() 