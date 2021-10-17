from pyvarml.utils.retriever import FTP

foo = FTP()

if foo.retrieve_package(category="classification"): # Change here
    print(f"Model: {foo.model}")
    print(f"Label: {foo.label}")
