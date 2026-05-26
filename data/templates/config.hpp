class CfgPatches
{
    class ADDON
    {
        name = "%MOD_NAME% - Templates";
        requiredVersion = 2.06;
        requiredAddons[] = {"A3A_core", "A3A_ultimate"};
        author = "%AUTHOR_NAME%";
        authors[] = {};
        authorUrl = "%AUTHOR_URL%";
    };
};

class A3A
{
    class Templates
    {#
        class %MOD_NAME%_%SIDE%
        {
            side = "%SIDE%";
            name = "%SIDE_NAME%";
            description = "%SIDE_DESCRIPTION%";
            flagTexture = "%SIDE_FLAG_TEXTURE%";
            basepath = "%SIDE_BASE_PATH%";
            file = "%SIDE_TEMPLATE_FILE_NO_EXT%";
        };#
    };
};