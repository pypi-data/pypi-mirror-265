from setuptools import setup
from pathlib import Path

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()
setup(
  name="vite-project",
  version="1.0.4",
  package_dir={"react_app": "dist"},
  package_data={"react_app": ["**/*.*"]},
  long_description=long_description,
  long_description_content_type="text/markdown"
)
