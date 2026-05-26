from string import Template

CONFIG_TEMPLATE = Template("""
class CfgPatches
{
    class ADDON
    {
        name = "${mod_name} - templates";
        requiredVersion = 2.06;
        requiredAddons[] = {"A3A_core", "A3A_ultimate"};
        author = "${author_name}";
        authors[] = { "${author_name}" };
        authorUrl = "${author_url}";
    };
};

class A3A
{
    class Templates
    {
        ${side_templates}
    };
};
""")

SIDE_TEMPLATE = Template("""
        class ${mod_name}_${side}
        {
            side = "${side}";
            name = "${side_name}";
            description = "${side_description}";
            flagTexture = "${side_flag}";
            basepath = "${side_path}";
            file = "${side_file_name}";
        };
""")