#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <vector>
using namespace std;

map<string, string> names;

int main(int argc, char *argv[])
{
    void species_mapping();
    double FM2Can(const double &c, const string &na, const string &s, const string &n2);

    double chi_f=stod(argv[1]);
    // read the species name mapping between FlameMaster and Chemkin/Cantera
    species_mapping();

    ifstream fstrm("input");
    // check input file
    if(!fstrm.is_open())
        throw runtime_error("File input not found");
    // read information from input
    string fuel,chi,TOF;
    getline(fstrm,fuel);
    getline(fstrm,TOF);
    vector<double> chi_st;
    while(getline(fstrm,chi)){
        chi_st.push_back(FM2Can(chi_f,fuel,chi,TOF));
    }
    // fsrtm.close();
    // write the chi_param.include file
    ofstream chi_out("tables/chi_param.include");
    chi_out << "chi_param" << endl;
    chi_out << chi_st.size() << endl;
    chi_out << "(" << endl;
    for(auto &r : chi_st)
        chi_out << scientific << r << endl;
    chi_out << ");";
    return 0;
}

void species_mapping()
{
    // mixture fraction and temperature
    // names.insert({"Z","Z"});
    // names.insert({"temperature","T"});
    // read in species translate file
    ifstream fstrm;
    fstrm.open("speciestranslated");
    if(!fstrm.is_open())
        throw runtime_error("File speciestranslated not found");
    string line;
    while(getline(fstrm, line)){
        istringstream sstrm(line);
        string name_FM, name_CK;
        sstrm >> name_CK >> name_FM;
        names.insert({name_FM,name_CK});
    }
    // output to check
    // for ( const auto &w : names )
    //     cout << w.first << " " << w.second << endl;
}

double FM2Can(const double &chi_f, const string &fuel, const string &chi, const string &TOF)
{
    vector<double> data_read(ifstream &fstrm, const int &pts);

    string filename = fuel+chi+TOF;
    ifstream FM_file(filename);
    if(!FM_file.is_open())
        throw runtime_error("File "+filename+" not found");
    cout << "Reading " << filename << endl;
    int grid_pts;
    string line;
    while(getline(FM_file,line)){
        // the position of gridPoints is 0
        if(!line.find("gridPoints")){
            grid_pts=stoi(line.substr(line.find_first_of("0123456789")));
            // cout << grid_pts << endl;
            getline(FM_file,line);
            getline(FM_file,line);
            break;
        }
    }

    // data
    vector<string> var_name;
    vector<vector<double>> all_data;

    // mixture fraction
    getline(FM_file,line);
    var_name.push_back("Z");
    all_data.push_back(data_read(FM_file,grid_pts));

    // temperature
    getline(FM_file,line);
    var_name.push_back("T");
    all_data.push_back(data_read(FM_file,grid_pts));

    // species
    for(int i=0;i!=names.size();++i)
    {
        getline(FM_file,line);
        string FM_name=line.substr(line.find("-")+1);
        // translate FM_name to CK_name
        // cout << names[FM_name] << endl;
        var_name.push_back(names[FM_name]);
        all_data.push_back(data_read(FM_file,grid_pts));
    }

    // skip W and ZBilger
    getline(FM_file,line);
    data_read(FM_file,grid_pts);
    getline(FM_file,line);
    data_read(FM_file,grid_pts);

    // scalar dissipation rate
    getline(FM_file,line);

    //var_name.push_back("chi");
    //all_data.push_back(data_read(FM_file,grid_pts));
    var_name.insert(var_name.begin()+2,"chi");
    all_data.insert(all_data.begin()+2,data_read(FM_file,grid_pts));

    // skip density, lambda, cp, lambdaOverCp
    getline(FM_file,line);
    data_read(FM_file,grid_pts);
    getline(FM_file,line);
    data_read(FM_file,grid_pts);
    getline(FM_file,line);
    data_read(FM_file,grid_pts);
    getline(FM_file,line);
    data_read(FM_file,grid_pts);

    // viscosity
    getline(FM_file,line);
    var_name.push_back("mu");
    all_data.push_back(data_read(FM_file,grid_pts));

    // write to Table_chi.csv
    // make filename for Cantera tables
    ostringstream strm;
    strm << stod(chi);
    filename = "tables/Table_"+strm.str()+".csv";
    cout << "Writing " << filename << endl;
    ofstream out_file(filename);

    // names of variable
    for(int i=0;i!=var_name.size()-1;++i)
        out_file << var_name[i] << ',';
    out_file << var_name[var_name.size()-1] << endl;

    // data
    for(int j=0;j!=grid_pts;++j)
    {
        for(int i=0;i!=var_name.size()-1;++i)
            out_file << scientific << all_data[i][j] << ',';
        out_file << scientific << all_data[var_name.size()-1][j] << endl;
    }

    out_file.close();
    
    // check the whether output mixture fraction
    if ( stod(chi) == chi_f )
    {
        out_file.open("tables/Z_param.include");
        out_file << "Z_param" << endl;
        out_file << all_data[0].size() << endl;
        out_file << "(" << endl;
        for(auto &r : all_data[0])
            out_file << scientific << r << endl;
        out_file << ");";
    }

    return stod(chi);
}

vector<double> data_read(ifstream &fstrm, const int &pts)
{
    double data_buff;
    string line;
    vector<double> var_data;
    for(int i=0;i!=pts;++i)
    {
        fstrm >> data_buff;
        var_data.push_back(data_buff);
    }
    getline(fstrm,line);
    return var_data;
}
