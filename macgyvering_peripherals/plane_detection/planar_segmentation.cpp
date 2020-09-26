#include <iostream>
#include <vector>
#include <fstream>

#include <pcl/common/colors.h>
#include <pcl/common/centroid.h>

#include <pcl/ModelCoefficients.h>
#include <pcl/point_types.h>

#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/io/openni_grabber.h>

#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>

#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>

#include <pcl/visualization/cloud_viewer.h>

#include <pcl/features/normal_3d.h>

#include <pcl/filters/extract_indices.h>
#include <pcl/filters/passthrough.h>
#include <pcl/filters/statistical_outlier_removal.h>

#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>

using namespace std;
using namespace pcl;

visualization::CloudViewer viewer ("Segmented Point Cloud");
bool saveCloud = true;
bool saveFile = true; //Save mean positions of objects to a file

void workspace_filter(PointCloud<PointXYZRGBA>::Ptr &cloud, PointCloud<PointXYZRGBA>::Ptr &cloud_filtered)
{
	// Filter within the robot workspace - (-0.25, 0.25) is a good working range;
	PassThrough<PointXYZRGBA> pass;

	// Working range of robot workspace for side Kinect is "y" = [-0.25,0.25]
	// Working range of robot workspace for top Kinect is "y" = [-0.32, 0.05] and "x" = [-0.31,0.35]

	//Uncomment following for side Kinect
	/*pass.setFilterFieldName("y");
	pass.setFilterLimits(-0.25,0.25); // Working range of robot workspace for side Kinect is [-0.25,0.25]
	pass.setInputCloud(cloud);
	pass.filter(*cloud_filtered);*/

	//Uncomment following for bracket mounted Kinect
	pass.setFilterFieldName("y");
	pass.setFilterLimits(-1.0, 0.05);
	pass.setInputCloud(cloud);
	pass.filter(*cloud_filtered);

	pass.setFilterFieldName("x");
	pass.setFilterLimits(-0.32,0.4);
	pass.setInputCloud(cloud_filtered);
	pass.filter(*cloud_filtered);
}

void outlier_remove(PointCloud<PointXYZRGBA>::Ptr &cloud, PointCloud<PointXYZRGBA>::Ptr &cloud_filtered)
{
	//For side Kinect, MeanK = 50
	//Outlier removal
	StatisticalOutlierRemoval<PointXYZRGBA> sor;
	sor.setInputCloud(cloud);
	sor.setMeanK(50);
	sor.setStddevMulThresh(1.0);
	sor.filter(*cloud_filtered);
}

void object_segmentation(PointCloud<PointXYZRGBA>::Ptr &cloud, PointCloud<PointXYZRGBA>::Ptr &cloud_seg)
{

	//Cluster the point cloud
	search::KdTree<PointXYZRGBA>::Ptr tree(new search::KdTree<PointXYZRGBA>);
	tree->setInputCloud(cloud);
	vector<PointIndices> cluster_indices;
	EuclideanClusterExtraction<PointXYZRGBA> ec;
	ec.setClusterTolerance(0.02);
	ec.setMinClusterSize(100);
	ec.setMaxClusterSize(25000);
	ec.setSearchMethod(tree);
	ec.setInputCloud(cloud);
	ec.extract(cluster_indices);

	int i = 0;
	vector<PointXYZ> center_points;

	GlasbeyLUT colors;
	for (vector<PointIndices>::const_iterator it = cluster_indices.begin(); it != cluster_indices.end(); ++it)
	{
		PointCloud<PointXYZRGBA>::Ptr objects(new PointCloud<PointXYZRGBA>);

		CentroidPoint<PointXYZRGBA> centroid;
		PointXYZ obj_centroid;

		for (vector<int>::const_iterator pit = it->indices.begin(); pit != it->indices.end(); ++pit)
		{
			PointXYZRGBA pointRGB =  cloud->points[*pit];
			pointRGB.r = colors.at(i).r;
			pointRGB.g = colors.at(i).g;
			pointRGB.b = colors.at(i).b;

			centroid.add(pointRGB);

			cloud_seg->points.push_back(pointRGB); //For visualizing the entire segmented point cloud
			objects->points.push_back(pointRGB); //For visualizing the individual objects
		}

		//Determine object poses (centroids)
		centroid.get(obj_centroid);
		//cout << obj_centroid << endl;
		center_points.push_back(obj_centroid);

		//Save point cloud
		if (saveCloud)
		{
			stringstream stream;
			stream << "inputCloud" << i << ".ply";
			string filename = stream.str();

			if (io::savePLYFile(filename, *objects) == 0)
			{
				cout << "Saved " << filename << "." << endl;
			}
			else
				PCL_ERROR("Problem saving the file");
		}

		i++;
	}


	//Save centroids to a file
	if (saveFile)
	{
		cout << "Saving object positions to a file" << endl;

		ofstream mean_pos_file;
		mean_pos_file.open("Object_positions.csv");

		for (vector<PointXYZ>::const_iterator it = center_points.begin(); it != center_points.end(); ++it)
		{
			mean_pos_file << it->x << "," << it->y << "," << it->z << "\n";
		}	

		mean_pos_file.close();			
	}

	if (saveCloud)
	{
		stringstream stream;
			stream << "fullCloud.ply";
			string filename = stream.str();

			if (io::savePLYFile(filename, *cloud_seg) == 0)
			{
				cout << "Saved " << filename << "." << endl;
			}
			else
				PCL_ERROR("Problem saving the file");
	}

	saveFile = false;
	saveCloud = false;
}

void plane_segment(const PointCloud<PointXYZRGBA>::ConstPtr &cloud)
{
	//Distance threshold for side Kinect is 0.0078
	//Distance threshold for top Kinect is 0.009 (the higher, more strict)

	PointCloud<PointXYZRGBA>::Ptr cloud_out(new PointCloud<PointXYZRGBA>);
	PointCloud<PointXYZRGBA>::Ptr cloud_pass(new PointCloud<PointXYZRGBA>);
	PointCloud<PointXYZRGBA>::Ptr cloud_filtered(new PointCloud<PointXYZRGBA>);
	PointCloud<PointXYZRGBA>::Ptr cloud_seg(new PointCloud<PointXYZRGBA>);

	SACSegmentation<PointXYZRGBA> seg;
	PointIndices::Ptr inliers(new PointIndices);
	ModelCoefficients * model_coefficients = new ModelCoefficients;

	//cout << "Point cloud data: " << cloud->points.size() << " points" << endl;

	seg.setInputCloud(cloud);
	seg.setModelType(SACMODEL_PLANE);
	seg.setMethodType(SAC_RANSAC);
	seg.setDistanceThreshold(0.0085);	//0.0075 //0.0006	
	seg.segment(*inliers, *model_coefficients);

	if (inliers->indices.size() == 0)
	{
		PCL_ERROR("Could not estimate planar model");
	}
	else
	{
		//cout << "Inliers estimated" << endl;

		//copyPointCloud(*cloud, inliers->indices, *cloud_out);
		ExtractIndices<PointXYZRGBA> filter;
		filter.setInputCloud(cloud);
		filter.setIndices(inliers);
		filter.setNegative(true);
		filter.filter(*cloud_out);

		//Filter within workspace
		workspace_filter(cloud_out, cloud_pass);
		//Remove any spurious points or outliers
		outlier_remove(cloud_pass, cloud_filtered);
		//Segment the resultant point cloud
		object_segmentation(cloud_filtered, cloud_seg);

		if (!viewer.wasStopped())
		{
			//viewer.showCloud(cloud_out);
			//viewer.showCloud(cloud_filtered);
			viewer.showCloud(cloud_seg);
		}
		
	}
}

int main(int argc, char** argv)
{

	Grabber * interface = new OpenNIGrabber();

	boost::function<void (const PointCloud<PointXYZRGBA>::ConstPtr &)> f = boost::bind(&plane_segment, _1);

	interface->registerCallback(f);
	interface->start();

	while (!viewer.wasStopped())
	{
		boost::this_thread::sleep(boost::posix_time::seconds(1));
	}

	interface->stop();

	return 0;

}