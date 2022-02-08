import sys
import boto3


def put_parameters(region: str, parameters, from_path: str, to_path: str):
    ssm = boto3.client("ssm", region_name=region)
    for parameter in parameters["Parameters"]:
        try:
            ssm.put_parameter(
                Name=parameter["Name"].replace(from_path, to_path),
                Value=parameter["Value"],
                Type=parameter["Type"],
                Overwrite=True,
            )
        except Exception as e:
            print(e)


def get_parameters_by_path(region: str, path: str, next_token: str = None):
    ssm = boto3.client("ssm", region_name=region)
    params = {"Path": path, "Recursive": True, "WithDecryption": True}
    if next_token:
        params["NextToken"] = next_token
    return ssm.get_parameters_by_path(**params)


if __name__ == "__main__":
    from_region, to_region, from_path, to_path = sys.argv[1:]

    parameters = get_parameters_by_path(from_region, f"/{from_path}", None)
    put_parameters(to_region, parameters, from_path, to_path)

    while "NextToken" in parameters:
        parameters = get_parameters_by_path(
            from_region, f"/{from_path}", parameters["NextToken"]
        )
        put_parameters(to_region, parameters, from_path, to_path)
