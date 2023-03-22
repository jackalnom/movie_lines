from fastapi import APIRouter
import os
import pkg_resources

router = APIRouter()

def calc_container(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

@router.get("/team/")
def version():
    return "Lucas"

@router.get("/version/")
def version():
    return "1.1"

@router.get("/pkgsize/")
def get_pkgsize():
    dists = [d for d in pkg_resources.working_set]

    message = []
    for dist in dists:
        try:
            path = os.path.join(dist.location, dist.project_name)
            size = calc_container(path)
            if size / 1000 > 1.0:
                message.append(
                    {"dist": dist.project_name, "size_in_mb": size / (1000 * 1000)}
                )
        except OSError:
            "{} no longer exists".format(dist.project_name)

    message = sorted(message, key=lambda d: d["size_in_mb"], reverse=True)
    return {"message": message}
