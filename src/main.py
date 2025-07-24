import uvicorn
from tl import tlinks

def main():
    uvicorn.run(tlinks, host='localhost', port=8080)


if __name__ == "__main__":
    main()
